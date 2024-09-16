r""" 
Içi, vous retrouverez les variables d'environnements utilisées par le l1test_backend
-----------------------------------------------------------------------------------

Il n'existe pas de moyens pour acheminer les données necessaires au traitement 
de la commande par l1test_backend. Pour cela, les plugins backend existant passent 
par enregistrer les données comme variable d'environement, ainsi le l1test_backend 
peut retrouver la donnée et décider comment executer ses tests. 

Note: Les variables d'environnements ne persistent pas après la fermeture de Thonny.
"""

# `IMPORT_MODULE_VAR` est une variable d'environnment qui stocke la valeur de l'option
# `l1test_options.IMPORT_MODULE` qui indique si oui(`True`) ou non(`False`) qu'il faut
# importer le module executé dans le shell.
IMPORT_MODULE_VAR = "import_module"

# LINENO est une variable d'environnement qui stocke le numéro de la ligne du test à executer.
LINENO = "lineno"

# FILTER_PREDICATE_VAR n'est pas une variable d'environnement mais nom de la donnée qui 
# stocke le prédicat qui permet de filtrer les tests à executer.
FILTER_PREDICATE_VAR = "filter_predicate"

# IS_GUI_MODE_VAR est une variable d'environnement qui stocke si L1test est en mode GUI 
# ou en mode console.
IS_GUI_MODE_VAR = "is_gui_mode"