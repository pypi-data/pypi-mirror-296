from DLMSAdapter import Adapter, AdapterException


_adapters: tuple[Adapter] | None = None

def get_adapters() -> tuple[Adapter]:
    if _adapters is None:
        raise AdapterException("adapters with not setting")
    return _adapters


def set_adapters(value: tuple[Adapter]):
    global _adapters
    _adapters = value

