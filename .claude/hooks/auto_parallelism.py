#!/usr/bin/env python3
"""
Auto-Parallelism Hook
Ajusta paralelismo baseado em recursos disponíveis
Matcher: SessionStart
"""

import os
import sys
import json
from pathlib import Path


def get_memory_gb():
    """Retorna RAM disponível em GB"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    meminfo[key.strip()] = int(value.split()[0])

        total_kb = meminfo['MemTotal']
        mem_free = meminfo.get('MemAvailable', meminfo.get('MemFree', 0))
        buffers = meminfo.get('Buffers', 0)
        cached = meminfo.get('Cached', 0)

        # Disponível real
        avail_kb = min(mem_free + buffers + cached, total_kb)
        return {
            'total': round(total_kb / (1024 * 1024), 1),
            'available': round(avail_kb / (1024 * 1024), 1)
        }
    except Exception:
        return {'total': 16, 'available': 8}


def calculate_parallelism(mem_total_gb, cpu_cores):
    """
    Calcula parallelism baseado em RAM TOTAL do sistema
    OTIMIZADO: Usa 50% da RAM (era 40%) para mais agentes

    OTIMIZADO para maior throughput:
    - 8GB total: 2 agentes (era 1-2)
    - 16GB total: 3-4 agentes (era 2-3) ← MELHORIA
    - 24GB total: 4-5 agentes (era 3-4) ← MELHORIA
    - 32GB total: 5-7 agentes (era 4-6) ← MELHORIA
    - 64GB+: 7-8 agentes (era 6-8) ← MELHORIA

    Deixa ±50% da RAM pro OS + apps do usuário (era 60%)
    """

    # OTIMIZAÇÃO: 50% da RAM pro Claude (era 40%)
    mem_for_claude = mem_total_gb * 0.5

    # Cada agente usa ±1.5-2GB em média
    # OTIMIZAÇÃO: Thresholds ajustados para mais agentes
    if mem_total_gb >= 64:
        parallelism = 7  # era 6
    elif mem_total_gb >= 32:
        parallelism = 5  # era 4
    elif mem_total_gb >= 24:
        parallelism = 4  # era 3
    elif mem_total_gb >= 15:  # NOVO: 15GB+ → 3 agentes
        parallelism = 3
    elif mem_total_gb >= 10:  # 10-14GB → 2 agentes
        parallelism = 2
    else:
        parallelism = 1

    # OTIMIZAÇÃO: Limita por CPU também (máx 60% dos cores, era 50%)
    cpu_limit = max(1, int(cpu_cores * 0.6))

    return max(1, min(parallelism, cpu_limit))


def update_agent_parallelism(parallelism: int, orchestrator_parallelism: int, agents_dir: Path):
    """Atualiza parallelism nos arquivos de agentes (apenas se necessário)"""

    # Agentes que sempre devem ter parallelism=1
    fixed_agents = {'oracle', 'meta-agent', 'code-search'}

    updated = []

    for agent_file in agents_dir.glob('*.md'):
        agent_name = agent_file.stem

        # Preserva fixed agents
        if agent_name in fixed_agents:
            continue

        content = agent_file.read_text()
        target = orchestrator_parallelism if agent_name == 'orchestrator-expert' else parallelism

        # Verifica se já tem o parallelism correto
        for line in content.split('\n'):
            if 'parallelism:' in line and not line.strip().startswith('#'):
                try:
                    current = int(line.split('parallelism:')[1].strip())
                    if current != target:
                        new_content = content.replace(
                            f'parallelism: {current}',
                            f'parallelism: {target}'
                        )
                        agent_file.write_text(new_content)
                        updated.append(agent_name)
                except ValueError:
                    pass  # Erro ao parsear, ignora
                break

    return updated


def main():
    cwd = Path.cwd()
    agents_dir = cwd / '.claude' / 'agents'
    config_file = cwd / '.claude' / 'auto_config.json'

    # Detecta recursos
    mem = get_memory_gb()
    cpu_cores = os.cpu_count() or 4

    # Calcula parallelism (baseado em RAM TOTAL, não disponível)
    parallelism = calculate_parallelism(mem['total'], cpu_cores)
    orchestrator_parallelism = max(1, parallelism - 1) if parallelism > 1 else 1

    # Salva config
    config = {
        'parallelism': parallelism,
        'orchestrator_parallelism': orchestrator_parallelism,
        'memory_gb': mem,
        'cpu_cores': cpu_cores,
        'updated_at': str(os.times()[4])
    }

    config_file.write_text(json.dumps(config, indent=2))

    # Atualiza agentes (incluindo orchestrator)
    updated = update_agent_parallelism(parallelism, orchestrator_parallelism, agents_dir)

    # Log silencioso (só mostra se mudou algo)
    if updated:
        print(f"🧠 Auto-parallelism: {mem['available']}GB RAM → {parallelism} agents (updated {len(updated)} files)")
    else:
        print(f"🧠 Auto-parallelism: {mem['available']}GB RAM → {parallelism} agents (already configured)")

    sys.exit(0)


if __name__ == "__main__":
    main()
