"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from Utilities.compiler import compile_module

compile_module(root='..\\Release\\CNSimSnatcher', mod_scripts_folder='./SimSnatcher', include_folders=('cnsimsnatcher', 'ssutilities'), mod_name='cn_simsnatcher')
