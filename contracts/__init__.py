"""Layer contracts and protocols.

All contracts are Protocol types (structural subtyping from typing module).
No implementation. Only interface definitions and invariants.

Canonical contracts:
- amanecer_to_fenix: extraction -> rule loading
- fenix_to_arana: rule loading -> evaluation
- arana_to_ire: evaluation -> reporting
- adapter_to_core: external adapters -> core engine
"""

from .amanecer_to_fenix import AmanecerOutput, FenixInput
from .fenix_to_arana import FenixOutput, AranaInput
from .arana_to_ire import AranaOutput, IreInput
from .adapter_to_core import AdapterInput, CoreOutput

__all__ = [
    'AmanecerOutput', 'FenixInput',
    'FenixOutput', 'AranaInput',
    'AranaOutput', 'IreInput',
    'AdapterInput', 'CoreOutput',
]
