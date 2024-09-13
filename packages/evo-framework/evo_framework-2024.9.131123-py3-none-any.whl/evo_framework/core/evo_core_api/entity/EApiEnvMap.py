#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiEnv import EApiEnv
#========================================================================================================================================
"""EApiEnvMap

    
    
"""
class EApiEnvMap(EObject):

    VERSION:str="7695fb2c403f737a789c04f41a7ab7d953a91092b132bc92ff0c319bbbf78ef9"

    def __init__(self):
        super().__init__()
        
        self.mapEApiEnv:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapEApiEnv, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapEApiEnv = self._doReadMap(EApiEnv, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapEApiEnv:{self.mapEApiEnv}",
                            ]) 
        return strReturn
    