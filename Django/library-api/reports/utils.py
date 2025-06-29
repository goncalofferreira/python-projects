def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def add_user_throttle_headers(request, response, view, throttle_class):
    """
    Se o user estiver autenticado, adiciona X-Throttle-Limit e X-Throttle-Remaining ao response.
    """
    if not request.user.is_authenticated:
        return response

    throttle = throttle_class()
    # Obtém a cache key que o DRF já definiu para esta request
    key = throttle.get_cache_key(request, view)
    if not key:
        return response

    # Procura o histórico de timestamps gravados na cache
    history = throttle.cache.get(key, [])

    # Calcula limites
    limit = throttle.get_rate()         # e.g. "100/day"
    remaining = max(0, throttle.num_requests - len(history))

    # Adiciona ao header
    response['X-Throttle-Limit'] = limit
    response['X-Throttle-Remaining'] = remaining
    return response

