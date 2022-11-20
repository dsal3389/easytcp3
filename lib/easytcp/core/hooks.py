import asyncio
from collections import defaultdict
from typing import Callable, Dict, Any, Tuple


class HookFactory:
    
    def __init__(self) -> None:
        self._hooks: Dict[str, List[Callable]] = defaultdict(list)

    def __getattr__(self, hook: str) -> Callable:
        return lambda func: self._register_hook(hook, func)

    async def call(self, hook: str, *args, **kwargs) -> Tuple(Any, ...):
        hook_funcs = self._hooks.get(hook, [])
        results, _ = await asyncio.wait(
            list(func(*args, **kwargs) for func in hook_funcs)
        )
        return results

    def _register_hook(self, hook: str, func: Callable) -> Callable:
        async def hook_wrapper(*args, **kwargs):
            if not asyncio.iscoroutinefunction(func):
                return func(*args, **kwargs)
            return await func(*args, **kwargs)

        self._hooks[hook].append(hook_wrapper)
        return self._hooks[hook]