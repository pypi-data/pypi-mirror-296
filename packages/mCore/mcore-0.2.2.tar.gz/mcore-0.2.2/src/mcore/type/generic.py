from typing import Callable,Dict,Any,TypeVar, Union, Tuple, Generic,List
import asyncio
T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')
V = TypeVar('V', default=Any)

def NotFunction(obj):
    """
    Vérifie si un objet n'est pas une fonction.

    Description de l'élément :
    Retourne True si l'objet fourni n'est pas une fonction, sinon False.

    Utilisation de l'élément :
    Utilisez cette fonction pour déterminer si un objet n'est pas de type fonction.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à vérifier
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - bool : True si l'objet n'est pas une fonction, sinon False.

    Exemple de l'élément :
    >>> NotFunction(lambda x: x)
    False
    >>> NotFunction(42)
    True
    """
    return not callable(obj)
def is_not_function(obj):
    """
    Vérifie si un objet n'est pas une fonction.

    Description de l'élément :
    Retourne True si l'objet fourni n'est pas une fonction, sinon False.

    Utilisation de l'élément :
    Utilisez cette fonction pour déterminer si un objet n'est pas de type fonction.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à vérifier
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - bool : True si l'objet n'est pas une fonction, sinon False.

    Exemple de l'élément :
    >>> is_not_function(lambda x: x)
    False
    >>> is_not_function(42)
    True
    """
    return not callable(obj)
def AsType(value, type_):
    """
    Convertit une valeur à un type donné si elle ne l'est pas déjà.

    Description de l'élément :
    Force une valeur à être d'un type spécifique, la convertissant si nécessaire.

    Utilisation de l'élément :
    Utilisez cette fonction pour garantir qu'une valeur est d'un type donné, sinon la convertir.

    Liste des différents arguments :
    - value :
      a. Nom de l'argument : value
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : La valeur à vérifier ou convertir
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type souhaité pour la valeur
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Any : La valeur convertie ou originale.

    Exemple de l'élément :
    >>> AsType("42", int)
    42
    >>> AsType(42, int)
    42
    """
    return value if isinstance(value, type_) else type_(value)
def AsString(value):
    """
    Convertit une valeur en chaîne de caractères si elle ne l'est pas déjà.

    Description de l'élément :
    Cette fonction vérifie si une valeur est de type `str`. Si ce n'est pas le cas, elle essaie de la convertir en chaîne de caractères.

    Utilisation de l'élément :
    Utilisez cette fonction pour garantir qu'une valeur est une chaîne de caractères.

    Liste des différents arguments :
    - value :
      a. Nom de l'argument : value
      b. Type de l'argument : any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : La valeur à convertir
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - str : La valeur convertie en chaîne de caractères.

    Exemple de l'élément :
    >>> AsString(123)
    '123'
    """
    return AsType(value, str)
def Complete(obj):
    """
    Récupère un dictionnaire complet avec toutes ses clés et valeurs.

    Description de l'élément :
    Cette fonction retourne un nouveau dictionnaire contenant toutes les clés et valeurs de l'objet d'origine.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir une copie complète d'un dictionnaire.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le dictionnaire d'origine
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Le dictionnaire complet.

    Exemple de l'élément :
    >>> Complete({'a': 1, 'b': 2})
    {'a': 1, 'b': 2}
    """
    return {k: obj[k] for k in obj}
def Override(T1, T2):
    """
    Remplace le contenu du dictionnaire T1 par celui de T2.

    Description de l'élément :
    Cette fonction met à jour le dictionnaire T1 avec les clés et valeurs de T2, remplaçant celles existantes.

    Utilisation de l'élément :
    Utilisez cette fonction pour fusionner deux dictionnaires en écrasant les valeurs de T1 par celles de T2.

    Liste des différents arguments :
    - T1 :
      a. Nom de l'argument : T1
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Modifiable
      d. À quoi correspond l'argument : Le dictionnaire principal à modifier
      e. Valeur par défaut de l'argument : Aucun

    - T2 :
      a. Nom de l'argument : T2
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le dictionnaire avec les valeurs de remplacement
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Le dictionnaire T1 mis à jour.

    Exemple de l'élément :
    >>> Override({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
    {'a': 1, 'b': 3, 'c': 4}
    """
    T1.update(T2)
    return T1
def RecursivePartial(obj):
    """
    Crée une version partielle récursive d'un dictionnaire ou d'une liste.

    Description de l'élément :
    Cette fonction retourne un nouvel objet où chaque valeur du dictionnaire ou de la liste originale est remplacée par une version récursive partielle.

    Utilisation de l'élément :
    Utilisez cette fonction pour transformer récursivement les valeurs d'un dictionnaire ou d'une liste.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict ou list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à transformer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict ou list : L'objet transformé récursivement.

    Exemple de l'élément :
    >>> RecursivePartial({'a': {'b': 2}})
    {'a': {'b': 2}}
    """
    if isinstance(obj, dict):
        return {k: RecursivePartial(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [RecursivePartial(v) for v in obj]
    else:
        return obj
def ArrayOneOrMore(lst):
    """
    Vérifie qu'un tableau contient au moins un élément.

    Description de l'élément :
    Cette fonction lève une erreur si le tableau passé en argument est vide.

    Utilisation de l'élément :
    Utilisez cette fonction pour s'assurer qu'un tableau n'est pas vide.

    Liste des différents arguments :
    - lst :
      a. Nom de l'argument : lst
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Modifiable
      d. À quoi correspond l'argument : Le tableau à vérifier
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Le tableau vérifié, doit contenir au moins un élément.

    Exemple de l'élément :
    >>> ArrayOneOrMore([1, 2, 3])
    [1, 2, 3]
    >>> ArrayOneOrMore([])
    ValueError: Array must have one or more items.
    """
    if len(lst) < 1:
        raise ValueError("Array must have one or more items.")
    return lst
def RecursiveObjValueType(obj, type_):
    """
    Modifie récursivement un objet en assignant un type donné à ses valeurs.

    Description de l'élément :
    Cette fonction prend un objet (dictionnaire ou autre) et applique récursivement un type spécifié à toutes ses valeurs,
    en traitant également les sous-objets.

    Utilisation de l'élément :
    Utilisez cette fonction pour transformer un dictionnaire de manière récursive, en assignant un type particulier à toutes ses valeurs.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : object
      c. Autres propriétés de l'argument : Peut être de n'importe quel type
      d. À quoi correspond l'argument : L'objet à transformer
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à appliquer aux valeurs de l'objet
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Le dictionnaire modifié avec les types appliqués.

    Exemple de l'élément :
    >>> RecursiveObjValueType({'a': 1, 'b': {'c': 2}}, str)
    {'a': str, 'b': {'c': str}}
    """
    if isinstance(obj, dict):
        return {k: (type_ if isinstance(v, object) else RecursiveObjValueType(v, type_)) for k, v in obj.items()}
    else:
        return type_
def TypeObjectValues(obj, type_):
    """
    Transforme toutes les valeurs d'un objet en un type spécifié.

    Description de l'élément :
    Cette fonction crée un nouveau dictionnaire en appliquant un type spécifié à toutes les valeurs des clés de l'objet d'origine.

    Utilisation de l'élément :
    Utilisez cette fonction pour créer un dictionnaire où toutes les valeurs sont d'un type donné.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet d'origine
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à appliquer aux valeurs
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Le nouveau dictionnaire avec les types appliqués.

    Exemple de l'élément :
    >>> TypeObjectValues({'a': 1, 'b': 2}, str)
    {'a': str, 'b': str}
    """
    return {k: type_ for k in obj}
def NoExtraProperties(T, U):
    """
    Empêche l'ajout de propriétés supplémentaires à un objet.

    Description de l'élément :
    Cette fonction retourne un dictionnaire combinant T et U, en veillant à ce que les clés de U qui n'existent pas dans T soient définies comme None.

    Utilisation de l'élément :
    Utilisez cette fonction pour garantir qu'un objet ne contient pas de propriétés supplémentaires par rapport à un modèle donné.

    Liste des différents arguments :
    - T :
      a. Nom de l'argument : T
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet de base
      e. Valeur par défaut de l'argument : Aucun

    - U :
      a. Nom de l'argument : U
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à vérifier
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : L'objet combiné avec les propriétés supplémentaires supprimées.

    Exemple de l'élément :
    >>> NoExtraProperties({'a': 1}, {'a': 1, 'b': 2})
    {'a': 1, 'b': None}
    """
    return {**T, **{k: None for k in U if k not in T}}
def MakeObjKeysAsNever(keys):
    """
    Assigne une valeur None à toutes les clés d'une liste donnée.

    Description de l'élément :
    Cette fonction crée un dictionnaire avec des clés provenant d'une liste, assignant None à chacune d'elles.

    Utilisation de l'élément :
    Utilisez cette fonction pour générer un dictionnaire où chaque clé de la liste a pour valeur None.

    Liste des différents arguments :
    - keys :
      a. Nom de l'argument : keys
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : La liste de clés à traiter
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Un dictionnaire avec les clés et des valeurs None.

    Exemple de l'élément :
    >>> MakeObjKeysAsNever(['a', 'b'])
    {'a': None, 'b': None}
    """
    return {k: None for k in keys}
def RemoveTypeFromTuple(t, type_to_remove):
    """
    Supprime un type spécifique d'un tuple.

    Description de l'élément :
    Cette fonction retourne un nouveau tuple en omettant tous les éléments correspondant à un type spécifique.

    Utilisation de l'élément :
    Utilisez cette fonction pour filtrer un tuple en supprimant les éléments d'un type donné.

    Liste des différents arguments :
    - t :
      a. Nom de l'argument : t
      b. Type de l'argument : tuple
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le tuple d'origine
      e. Valeur par défaut de l'argument : Aucun

    - type_to_remove :
      a. Nom de l'argument : type_to_remove
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à supprimer du tuple
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - tuple : Un nouveau tuple sans les éléments du type spécifié.

    Exemple de l'élément :
    >>> RemoveTypeFromTuple((1, 'a', 2.0), int)
    ('a', 2.0)
    """
    return tuple(x for x in t if not isinstance(x, type_to_remove))
def GetTypeKeyFromObject(obj, type_):
    """
    Récupère les clés d'un objet dont les valeurs ne sont pas d'un type donné.

    Description de l'élément :
    Cette fonction retourne une liste de clés d'un objet, en excluant celles dont les valeurs sont d'un type spécifié.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir les clés d'un dictionnaire dont les valeurs ne sont pas d'un type particulier.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à analyser
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à exclure
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Les clés dont les valeurs ne sont pas du type spécifié.

    Exemple de l'élément :
    >>> GetTypeKeyFromObject({'a': 1, 'b': 'string'}, int)
    ['b']
    """
    return [k for k, v in obj.items() if not isinstance(v, type_)]
def RemoveTypeFromObj(obj, type_):
    """
    Supprime les paires clé-valeur d'un objet dont les valeurs sont d'un type donné.

    Description de l'élément :
    Cette fonction retourne un nouveau dictionnaire en omettant les paires clé-valeur dont les valeurs correspondent à un type spécifié.

    Utilisation de l'élément :
    Utilisez cette fonction pour filtrer un dictionnaire et supprimer les éléments d'un type donné.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à analyser
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à supprimer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Un nouveau dictionnaire sans les paires clé-valeur du type spécifié.

    Exemple de l'élément :
    >>> RemoveTypeFromObj({'a': 1, 'b': 'text', 'c': 3.5}, int)
    {'b': 'text', 'c': 3.5}
    """
    return {k: v for k, v in obj.items() if not isinstance(v, type_)}
def GetObjectKeysThatAreOfType(obj, type_):
    """
    Récupère les clés d'un objet dont les valeurs sont d'un type donné.

    Description de l'élément :
    Cette fonction retourne une liste de clés d'un objet, dont les valeurs correspondent à un type spécifié.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir les clés d'un dictionnaire dont les valeurs sont d'un type particulier.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à analyser
      e. Valeur par défaut de l'argument : Aucun

    - type_ :
      a. Nom de l'argument : type_
      b. Type de l'argument : type
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le type à rechercher
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Les clés dont les valeurs sont du type spécifié.

    Exemple de l'élément :
    >>> GetObjectKeysThatAreOfType({'a': 1, 'b': 'string', 'c': 2.5}, str)
    ['b']
    """
    return [k for k in obj if isinstance(obj[k], type_)]
def ForceStringKeyObject(obj):
    """
    Filtre un objet pour ne conserver que les paires clé-valeur où la clé est une chaîne.

    Description de l'élément :
    Cette fonction retourne un nouveau dictionnaire contenant uniquement les paires clé-valeur avec des clés de type chaîne.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir un dictionnaire avec uniquement des clés de type chaîne.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à filtrer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Un dictionnaire avec uniquement des clés de type chaîne.

    Exemple de l'élément :
    >>> ForceStringKeyObject({1: 'a', 'b': 2, 'c': 3})
    {'b': 2, 'c': 3}
    """
    return {k: v for k, v in obj.items() if isinstance(k, str)}
def Indices(arr):
    """
    Renvoie une liste d'indices pour un tableau donné.

    Description de l'élément :
    Cette fonction génère une liste d'indices correspondant aux positions des éléments dans un tableau.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir les indices d'un tableau.

    Liste des différents arguments :
    - arr :
      a. Nom de l'argument : arr
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le tableau dont on veut les indices
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Une liste d'indices du tableau.

    Exemple de l'élément :
    >>> Indices(['a', 'b', 'c'])
    [0, 1, 2]
    """
    return list(range(len(arr)))
def Writeable(obj):
    """
    Retourne l'objet d'origine.

    Description de l'élément :
    Cette fonction retourne l'objet tel quel, utile lorsque l'on travaille dans un contexte où la mutabilité est souhaitée.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir un objet qui peut être modifié.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à retourner
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - any : L'objet d'origine.

    Exemple de l'élément :
    >>> Writeable({'a': 1})
    {'a': 1}
    """
    return obj
def DeepWriteable(obj):
    """
    Rend tous les éléments d'un objet modifiables de manière récursive.

    Description de l'élément :
    Cette fonction traverse récursivement un objet et retourne une version modifiable de celui-ci.

    Utilisation de l'élément :
    Utilisez cette fonction pour rendre modifiable un objet composé de sous-éléments.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict ou list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à rendre modifiable
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict ou list : L'objet modifiable.

    Exemple de l'élément :
    >>> DeepWriteable({'a': [{'b': 2}]})
    {'a': [{'b': 2}]}
    """
    if isinstance(obj, dict):
        return {k: DeepWriteable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [DeepWriteable(v) for v in obj]
    else:
        return obj
def IsObject(obj):
    """
    Vérifie si un objet est un dictionnaire et non une fonction.

    Description de l'élément :
    Cette fonction retourne True si l'objet est un dictionnaire et n'est pas appelable.

    Utilisation de l'élément :
    Utilisez cette fonction pour déterminer si un objet est un dictionnaire.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'objet à vérifier
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - bool : True si l'objet est un dictionnaire, sinon False.

    Exemple de l'élément :
    >>> IsObject({'a': 1})
    True
    >>> IsObject(lambda x: x)
    False
    """
    return isinstance(obj, dict) and not callable(obj)
def ReadonlyDeep(obj):
    """
    Applique une transformation récursive pour rendre les valeurs d'un objet immuables.

    Description de l'élément :
    Cette fonction parcourt récursivement un objet, qu'il soit un dictionnaire ou une liste, pour en rendre les valeurs effectivement immuables en profondeur. Notez que Python ne possède pas nativement le concept de readonly, donc cette fonction est conceptuelle.

    Utilisation de l'élément :
    Utilisez cette fonction pour parcourir un objet complexe et le préparer de manière à éviter les modifications non intentionnelles.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : dict ou list
      c. Autres propriétés de l'argument : Peut contenir des sous-objets
      d. À quoi correspond l'argument : L'objet à traiter
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict ou list : Une version transformée de l'objet d'entrée, conceptuellement immuable.

    Exemple de l'élément :
    >>> ReadonlyDeep({'a': 1, 'b': {'c': 2}})
    {'a': 1, 'b': {'c': 2}}
    >>> ReadonlyDeep([1, [2, 3]])
    [1, [2, 3]]
    """
    if isinstance(obj, dict):
        return {k: ReadonlyDeep(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ReadonlyDeep(v) for v in obj]
    else:
        return obj
def Exclusive(A, B, C={}, D={}, E={}):
    """
    Génère des combinaisons exclusives entre plusieurs objets.

    Description de l'élément :
    Cette fonction retourne une liste de dictionnaires représentant les combinaisons exclusives de propriétés entre plusieurs objets. Chaque objet est combiné avec les propriétés non partagées des autres.

    Utilisation de l'élément :
    Utilisez cette fonction pour créer des ensembles d'objets où chaque ensemble est défini par des propriétés exclusives.

    Liste des différents arguments :
    - A, B, C, D, E :
      a. Nom de l'argument : A, B, C, D, E
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Peut contenir des clés multiples
      d. À quoi correspond l'argument : Les objets à combiner
      e. Valeur par défaut de l'argument : C, D, E par défaut à des dictionnaires vides

    Type de retour de l'élément :
    - list : Une liste de dictionnaires, chaque dictionnaire étant une combinaison exclusive.

    Exemple de l'élément :
    >>> Exclusive({'a': 1}, {'b': 2})
    [{'a': None, 'b': 2}, {'b': None, 'a': 1}]
    """
    return [
        {**{k: None for k in set(A.keys()).union(C.keys()).union(D.keys()).union(E.keys()).difference(B.keys())}, **B},
        {**{k: None for k in set(B.keys()).union(C.keys()).union(D.keys()).union(E.keys()).difference(A.keys())}, **A},
        {**{k: None for k in set(B.keys()).union(A.keys()).union(D.keys()).union(E.keys()).difference(C.keys())}, **C},
        {**{k: None for k in set(B.keys()).union(A.keys()).union(C.keys()).union(E.keys()).difference(D.keys())}, **D},
        {**{k: None for k in set(B.keys()).union(A.keys()).union(C.keys()).union(D.keys()).difference(E.keys())}, **E}
    ]
def StringAndUnion(value):
    """
    Convertit une valeur en chaîne si elle n'est pas déjà de type chaîne.

    Description de l'élément :
    Cette fonction vérifie si une valeur est de type chaîne, sinon elle la convertit en chaîne. Elle est utilisée pour garantir que la sortie est toujours une chaîne.

    Utilisation de l'élément :
    Utilisez cette fonction pour normaliser les types de données en chaînes.

    Liste des différents arguments :
    - value :
      a. Nom de l'argument : value
      b. Type de l'argument : any
      c. Autres propriétés de l'argument : Peut être de n'importe quel type
      d. À quoi correspond l'argument : La valeur à convertir
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - str : La valeur convertie en chaîne.

    Exemple de l'élément :
    >>> StringAndUnion(123)
    '123'
    >>> StringAndUnion('abc')
    'abc'
    """
    return value if isinstance(value, (str, type(value))) else str(value)
def ArrayKeys(arr):
    """
    Récupère les indices d'un tableau sous forme de liste.

    Description de l'élément :
    Cette fonction prend un tableau (ou une liste) en entrée et retourne une liste contenant tous les indices de ce tableau.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir une liste d'indices correspondant aux positions des éléments dans un tableau donné. Cela peut être utile pour itérer sur les indices d'un tableau.

    Liste des différents arguments :
    - arr :
      a. Nom de l'argument : arr
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le tableau ou la liste dont on souhaite obtenir les indices
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Une liste d'entiers représentant les indices du tableau.

    Exemple de l'élément :
    >>> ArrayKeys(['a', 'b', 'c'])
    [0, 1, 2]

    >>> ArrayKeys([10, 20, 30, 40])
    [0, 1, 2, 3]
    """
    return list(range(len(arr)))
def combine(a: T, b: U) -> Union[T, U]:
    """
    Combine deux éléments en renvoyant l'un ou l'autre en fonction de leur type.

    Description de l'élément :
    Cette fonction simule une intersection de types en utilisant une union. Elle retourne un des deux éléments fournis basé sur une vérification de type.

    Utilisation de l'élément :
    Utilisez cette fonction pour combiner deux valeurs de types potentiellement différents et obtenir l'un des deux en fonction de leur type.

    Liste des différents arguments :
    - a :
      a. Nom de l'argument : a
      b. Type de l'argument : T
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le premier élément à comparer
      e. Valeur par défaut de l'argument : Aucun

    - b :
      a. Nom de l'argument : b
      b. Type de l'argument : U
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le second élément à comparer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Union[T, U] : L'un des deux éléments en fonction du type.

    Exemple de l'élément :
    >>> combine(10, "example")
    10
    >>> combine("test", 20)
    'test'
    """
    return a if isinstance(a, b.__class__) else b
def keys(obj: Any) -> list:
    """
    Récupère les clés d'un objet.

    Description de l'élément :
    Cette fonction retourne une liste des clés d'un objet, imitant la fonctionnalité keyof de TypeScript.

    Utilisation de l'élément :
    Passez un objet pour obtenir ses clés sous forme de liste.

    Liste des différents arguments :
    - obj :
      a. Nom de l'argument : obj
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Doit être un objet avec un dictionnaire de classe
      d. À quoi correspond l'argument : L'objet duquel on veut extraire les clés
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - list : Liste des clés de l'objet.

    Exemple de l'élément :
    >>> get_keys(Example())
    ['a', 'b']
    """
    return list(obj.__dict__.keys())
def map_types(d: Dict[str, Any], func: Callable[[Any], Any]) -> Dict[str, Any]:
    """
    Applique une fonction à toutes les valeurs d'un dictionnaire.

    Description de l'élément :
    Cette fonction utilise une compréhension de dictionnaire pour appliquer une fonction donnée à chaque valeur d'un dictionnaire.

    Utilisation de l'élément :
    Passez un dictionnaire et une fonction pour transformer les valeurs du dictionnaire.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : Dict[str, Any]
      c. Autres propriétés de l'argument : Un dictionnaire avec des clés de type str
      d. À quoi correspond l'argument : Le dictionnaire d'origine
      e. Valeur par défaut de l'argument : Aucun

    - func :
      a. Nom de l'argument : func
      b. Type de l'argument : Callable[[Any], Any]
      c. Autres propriétés de l'argument : Fonction qui accepte une valeur et renvoie une valeur
      d. À quoi correspond l'argument : La fonction à appliquer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Dict[str, Any] : Nouveau dictionnaire avec les valeurs modifiées.

    Exemple de l'élément :
    >>> map_types({'a': 1, 'b': 2}, lambda x: x * 2)
    {'a': 2, 'b': 4}
    """
    return {k: func(v) for k, v in d.items()}
def modify_mapping(d: Dict[str, Any], modifier: Callable[[Any], Any]) -> Dict[str, Any]:
    """
    Modifie toutes les valeurs d'un dictionnaire avec une fonction.

    Description de l'élément :
    Applique une fonction de modification à chaque valeur d'un dictionnaire.

    Utilisation de l'élément :
    Utilisez cette fonction pour transformer les valeurs d'un dictionnaire avec une fonction spécifiée.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : Dict[str, Any]
      c. Autres propriétés de l'argument : Un dictionnaire avec des clés de type str
      d. À quoi correspond l'argument : Le dictionnaire d'origine
      e. Valeur par défaut de l'argument : Aucun

    - modifier :
      a. Nom de l'argument : modifier
      b. Type de l'argument : Callable[[Any], Any]
      c. Autres propriétés de l'argument : Fonction qui accepte une valeur et renvoie une valeur
      d. À quoi correspond l'argument : La fonction de modification
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Dict[str, Any] : Nouveau dictionnaire avec les valeurs modifiées.

    Exemple de l'élément :
    >>> modify_mapping({'a': 1, 'b': 2}, lambda x: x + 1)
    {'a': 2, 'b': 3}
    """
    return {k: modifier(v) for k, v in d.items()}
def remap_keys(d: Dict[str, Any], remap: Dict[str, str]) -> Dict[str, Any]:
    """
    Remappe les clés d'un dictionnaire selon une correspondance donnée.

    Description de l'élément :
    Cette fonction change les clés d'un dictionnaire en utilisant un dictionnaire de remappage.

    Utilisation de l'élément :
    Utilisez cette fonction pour renommer les clés d'un dictionnaire selon un mappage spécifié.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : Dict[str, Any]
      c. Autres propriétés de l'argument : Un dictionnaire avec des clés de type str
      d. À quoi correspond l'argument : Le dictionnaire d'origine
      e. Valeur par défaut de l'argument : Aucun

    - remap :
      a. Nom de l'argument : remap
      b. Type de l'argument : Dict[str, str]
      c. Autres propriétés de l'argument : Un dictionnaire de correspondance de clés
      d. À quoi correspond l'argument : Le mappage des clés à appliquer
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Dict[str, Any] : Nouveau dictionnaire avec les clés remappées.

    Exemple de l'élément :
    >>> remap_keys({'a': 1, 'b': 2}, {'a': 'alpha'})
    {'alpha': 1, 'b': 2}
    """
    return {remap.get(k, k): v for k, v in d.items()}
def template_literal(name: str, age: int) -> str:
    """
    Génère une chaîne de caractères formatée à partir d'un nom et d'un âge.

    Description de l'élément :
    Cette fonction utilise les f-strings de Python pour créer une chaîne de caractères qui inclut un nom et un âge.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir une présentation formatée d'un individu avec son nom et son âge.

    Liste des différents arguments :
    - name :
      a. Nom de l'argument : name
      b. Type de l'argument : str
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le nom de la personne
      e. Valeur par défaut de l'argument : Aucun

    - age :
      a. Nom de l'argument : age
      b. Type de l'argument : int
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'âge de la personne
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - str : Une chaîne de caractères formatée.

    Exemple de l'élément :
    >>> template_literal("Alice", 30)
    'My name is Alice and I am 30 years old.'
    """
    return f"My name is {name} and I am {age} years old."
def partial_dict(d: Dict[str, Any], keys: list) -> Dict[str, Any]:
    """
    Crée un dictionnaire partiel en extrayant des clés spécifiées.

    Description de l'élément :
    Cette fonction génère un nouveau dictionnaire contenant uniquement les paires clé-valeur pour les clés spécifiées.

    Utilisation de l'élément :
    Utilisez cette fonction pour obtenir un sous-ensemble d'un dictionnaire basé sur une liste de clés.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le dictionnaire d'origine
      e. Valeur par défaut de l'argument : Aucun

    - keys :
      a. Nom de l'argument : keys
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Les clés à extraire
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Un dictionnaire contenant uniquement les clés spécifiées.

    Exemple de l'élément :
    >>> partial_dict({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
    {'a': 1, 'c': 3}
    """
    return {k: d[k] for k in keys if k in d}
def require_keys(d: Dict[str, Any], keys: list) -> bool:
    """
    Vérifie que toutes les clés requises sont présentes dans le dictionnaire.

    Description de l'élément :
    Cette fonction assure que toutes les clés spécifiées existent dans le dictionnaire donné.

    Utilisation de l'élément :
    Utilisez cette fonction pour valider la présence de clés essentielles dans un dictionnaire.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Le dictionnaire à vérifier
      e. Valeur par défaut de l'argument : Aucun

    - keys :
      a. Nom de l'argument : keys
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Les clés requises
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - bool : True si toutes les clés sont présentes, False sinon.

    Exemple de l'élément :
    >>> require_keys({'a': 1, 'b': 2}, ['a'])
    True
    >>> require_keys({'a': 1}, ['a', 'b'])
    False
    """
    return all(k in d for k in keys)
def create_record(keys: list, default_value: Any) -> Dict[str, Any]:
    """
    Crée un dictionnaire semblable à un enregistrement avec une valeur par défaut.

    Description de l'élément :
    Cette fonction génère un dictionnaire où chaque clé de la liste est associée à une valeur par défaut.

    Utilisation de l'élément :
    Utilisez cette fonction pour créer un enregistrement rapide d'un ensemble de clés avec une valeur par défaut.

    Liste des différents arguments :
    - keys :
      a. Nom de l'argument : keys
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : Les clés pour le dictionnaire
      e. Valeur par défaut de l'argument : Aucun

    - default_value :
      a. Nom de l'argument : default_value
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : La valeur par défaut à assigner
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Un dictionnaire avec les clés spécifiées et la valeur par défaut.

    Exemple de l'élément :
    >>> create_record(['x', 'y'], 0)
    {'x': 0, 'y': 0}
    """
    return {k: default_value for k in keys}
def omit_keys(d: Dict[str, Any], keys_to_omit: list) -> Dict[str, Any]:
    """
    Crée un nouveau dictionnaire en omettant les clés spécifiées.

    Description de l'élément :
    Cette fonction retourne un dictionnaire qui exclut les paires clé-valeur dont les clés sont spécifiées dans keys_to_omit.

    Utilisation de l'élément :
    Utilisez cette fonction pour filtrer un dictionnaire en supprimant les clés indésirables.

    Liste des différents arguments :
    - d :
      a. Nom de l'argument : d
      b. Type de l'argument : dict
      c. Autres propriétés de l'argument : Doit contenir des paires clé-valeur
      d. À quoi correspond l'argument : Le dictionnaire d'origine à filtrer
      e. Valeur par défaut de l'argument : Aucun

    - keys_to_omit :
      a. Nom de l'argument : keys_to_omit
      b. Type de l'argument : list
      c. Autres propriétés de l'argument : Liste des clés à omettre
      d. À quoi correspond l'argument : Les clés à retirer du dictionnaire
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - dict : Le dictionnaire filtré sans les clés omises.

    Exemple de l'élément :
    >>> omit_keys({'a': 1, 'b': 2, 'c': 3}, ['b'])
    {'a': 1, 'c': 3}
    """
    return {k: v for k, v in d.items() if k not in keys_to_omit}
def exclude_members(union_set: set, to_exclude: set) -> set:
    """
    Exclut les membres spécifiés d'un ensemble.

    Description de l'élément :
    Cette fonction retourne un nouvel ensemble en enlevant les éléments présents dans to_exclude de l'ensemble union_set.

    Utilisation de l'élément :
    Utilisez cette fonction pour soustraire un ensemble d'un autre.

    Liste des différents arguments :
    - union_set :
      a. Nom de l'argument : union_set
      b. Type de l'argument : set
      c. Autres propriétés de l'argument : Ensemble de base
      d. À quoi correspond l'argument : L'ensemble d'origine
      e. Valeur par défaut de l'argument : Aucun

    - to_exclude :
      a. Nom de l'argument : to_exclude
      b. Type de l'argument : set
      c. Autres propriétés de l'argument : Ensemble des éléments à exclure
      d. À quoi correspond l'argument : Les éléments à enlever de union_set
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - set : L'ensemble résultant après exclusion.

    Exemple de l'élément :
    >>> exclude_members({1, 2, 3}, {2})
    {1, 3}
    """
    return union_set - to_exclude
def extract_types(union_set: set, to_extract: set) -> set:
    """
    Extrait les membres spécifiés d'un ensemble.

    Description de l'élément :
    Cette fonction retourne un nouvel ensemble contenant seulement les éléments qui sont présents à la fois dans union_set et to_extract.

    Utilisation de l'élément :
    Utilisez cette fonction pour trouver l'intersection de deux ensembles.

    Liste des différents arguments :
    - union_set :
      a. Nom de l'argument : union_set
      b. Type de l'argument : set
      c. Autres propriétés de l'argument : Ensemble de base
      d. À quoi correspond l'argument : L'ensemble d'origine
      e. Valeur par défaut de l'argument : Aucun

    - to_extract :
      a. Nom de l'argument : to_extract
      b. Type de l'argument : set
      c. Autres propriétés de l'argument : Ensemble des éléments à extraire
      d. À quoi correspond l'argument : Les éléments à conserver de union_set
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - set : L'ensemble résultant après extraction.

    Exemple de l'élément :
    >>> extract_types({1, 2, 3}, {2, 3})
    {2, 3}
    """
    return union_set.intersection(to_extract)
def no_infer(value: Any) -> Any:
    """
    Démonstration de l'inférence de type en utilisant le typage dynamique de Python.

    Description de l'élément :
    Cette fonction retourne la valeur passée en argument sans effectuer de transformation. Elle illustre l'inférence de type dynamique de Python, où le type de la variable est déterminé à l'exécution.

    Utilisation de l'élément :
    Utilisez cette fonction lorsque vous souhaitez retourner une valeur sans la modifier, tout en démontrant que Python gère les types dynamiquement.

    Liste des différents arguments :
    - value :
      a. Nom de l'argument : value
      b. Type de l'argument : Any
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : La valeur à retourner
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Any : Retourne la même valeur que celle passée en argument, sans modification.

    Exemple de l'élément :
    >>> no_infer(42)
    42

    >>> no_infer("Hello")
    'Hello'

    >>> no_infer([1, 2, 3])
    [1, 2, 3]

    >>> no_infer({'key': 'value'})
    {'key': 'value'}
    """
    return value

class keyOf(Generic[T]):
    """
    Classe générique pour retourner une Union des clés ou des attributs d'un Dict ou d'un Object en utilisant la méthode __new__.
    
    Description de l'élément :
    Cette classe est conçue pour générer dynamiquement un type Union des clés d'un dictionnaire ou des attributs publics d'un objet.

    Utilisation de l'élément :
    Instanciez cette classe avec un dictionnaire ou un objet pour obtenir une Union des clés ou des attributs correspondants.

    Liste des différents arguments :
    - instance : 
      a. Nom de l'argument : instance
      b. Type de l'argument : T (TypeVar)
      c. Autres propriétés de l'argument : Aucun
      d. À quoi correspond l'argument : L'instance de l'objet ou du dictionnaire dont les clés ou attributs doivent être extraits.
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Union[Tuple[Any, ...]] : Une Union de tuples contenant les clés ou les attributs de l'instance d'entrée.
      Si l'instance est un dictionnaire, retourne une Union des tuples contenant toutes les clés du dictionnaire.
      Si l'instance est un objet, retourne une Union des tuples contenant tous les attributs publics de l'objet.
      Si l'instance n'est ni un dictionnaire ni un objet, retourne une Union vide.

    Exemple de l'élément :
    1. Pour un dictionnaire :
       example_dict = {'key1': 1, 'key2': 2}
       keys_union_dict = keyOf(example_dict)
       print(keys_union_dict)  # Output: Union['key1', 'key2']

    2. Pour un objet :
       class Example:
           def __init__(self):
               self.name = "Example"
               self.value = 42

       example_object = Example()
       keys_union_object = keyOf(example_object)
       print(keys_union_object)  # Output: Union['name', 'value']
    """

    def __new__(cls, instance: T) -> Union[Tuple[Any, ...]]:
        """
        Méthode __new__ pour créer une Union des clés d'un dictionnaire ou des attributs publics d'un objet.

        Arguments :
        - instance :
          a. Nom de l'argument : instance
          b. Type de l'argument : T (TypeVar)
          c. Autres propriétés de l'argument : Aucun
          d. À quoi correspond l'argument : L'instance de l'objet ou du dictionnaire dont les clés ou attributs doivent être extraits.
          e. Valeur par défaut de l'argument : Aucun

        Type de retour :
        - Union[Tuple[Any, ...]] : Une Union de tuples contenant les clés ou les attributs de l'instance d'entrée.
        """
        if isinstance(instance, dict):
            # Crée une Union des clés du dictionnaire
            return Union[Tuple[tuple(instance.keys())]]
        elif hasattr(instance, '__dict__'):
            # Crée une Union des attributs publics de l'objet
            return Union[Tuple[tuple(attr for attr in dir(instance) if not attr.startswith('_'))]]
        else:
            return Union[()]
class typeOf(Generic[T, K]):
    """
    Classe générique pour déterminer le type des valeurs associées aux clés ou attributs générés par keyOf[T].

    Description de l'élément :
    Cette classe est conçue pour obtenir le type des éléments dans un dictionnaire ou des attributs d'un objet en fonction des clés ou attributs spécifiés par keyOf[T].

    Utilisation de l'élément :
    Utilisez cette classe pour instancier un type qui représente les types des valeurs ou attributs des clés spécifiées dans un dictionnaire ou un objet.

    Liste des différents arguments :
    - T :
      a. Nom de l'argument : T
      b. Type de l'argument : TypeVar
      c. Autres propriétés de l'argument : Représente le dictionnaire ou l'objet
      d. À quoi correspond l'argument : Dict ou Object dont on veut connaître les types des valeurs
      e. Valeur par défaut de l'argument : Aucun

    - K :
      a. Nom de l'argument : K
      b. Type de l'argument : keyOf[T]
      c. Autres propriétés de l'argument : Représente les clés ou attributs de T
      d. À quoi correspond l'argument : Clés ou attributs dont on veut connaître les types de valeurs
      e. Valeur par défaut de l'argument : Aucun

    Type de retour de l'élément :
    - Le type des valeurs ou attributs correspondant aux clés ou attributs spécifiés par K dans T.

    Exemple de l'élément :
    1. Pour un dictionnaire :
       example_dict = {'key1': 10, 'key2': 'value'}
       keys = keyOf(example_dict)
       types_dict = typeOf(example_dict, keys)
       print(get_type_hints(types_dict))  # Output: {'key1': int, 'key2': str}

    2. Pour un objet :
       class Example:
           def __init__(self):
               self.name = "Example"
               self.value = 42

       example_object = Example()
       keys = keyOf(example_object)
       types_object = typeOf(example_object, keys)
       print(get_type_hints(types_object))  # Output: {'name': str, 'value': int}
    """

    def __new__(cls, instance: T, keys: keyOf[T]) -> Any:
        if isinstance(instance, dict):
            return {key: type(instance[key]) for key in keys}
        elif hasattr(instance, '__dict__'):
            return {attr: type(getattr(instance, attr)) for attr in keys}
        else:
            return {}
class CleValeur(Tuple[str, V], Generic[V]):
    """
    Classe représentant une paire clé-valeur générique, étendant Tuple[str, V].

    Cette classe permet de gérer des paires clé-valeur avec une clé de type chaîne de caractères
    et une valeur de type générique. Elle peut être utilisée là où un tuple clé-valeur est requis.

    Exemple d'utilisation :
    >>> paire = CleValeur("clé1", 100)
    >>> print(paire.cle)  # Affiche 'clé1'
    >>> print(paire.valeur)  # Affiche '100'
    """

    def __new__(cls, cle: str, valeur: V) -> 'CleValeur[V]':
        """
        Construit une nouvelle instance de CleValeur avec une clé et une valeur, en tant que tuple.

        Arguments :
        - cle (str) : La clé de la paire, doit être une chaîne de caractères.
        - valeur (V) : La valeur de la paire, peut être de tout type.

        Retour :
        - CleValeur[V] : Une nouvelle instance de CleValeur.

        Exemple :
        >>> CleValeur("clé1", 100)
        """
        return super().__new__(cls, (cle, valeur))

    @property
    def cle(self) -> str:
        """
        Retourne la clé de la paire clé-valeur.

        Retour :
        - str : La clé, qui est une chaîne de caractères.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire.cle
        'clé1'
        """
        return self[0]

    @property
    def valeur(self) -> V:
        """
        Retourne la valeur de la paire clé-valeur.

        Retour :
        - V : La valeur, qui peut être de tout type.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire.valeur
        100
        """
        return self[1]

    def __obtenir_paire__(self) -> Tuple[str, V]:
        """
        Retourne la paire (clé, valeur).

        Retour :
        - Tuple[str, V] : Un tuple contenant la clé et la valeur.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire.__obtenir_paire__()
        ('clé1', 100)
        """
        return self.cle, self.valeur

    def __repr__(self) -> Tuple[str, V]:
        """
        Retourne la paire (clé, valeur).

        Retour :
        - Tuple[str, V] : Un tuple contenant la clé et la valeur.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire.__obtenir_paire__()
        ('clé1', 100)
        """
        return self.cle, self.valeur

    def __call__(self) -> Tuple[str, V]:
        """
        Appelle l'instance pour obtenir directement la paire.

        Retour :
        - Tuple[str, V] : Un tuple contenant la clé et la valeur.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire()
        ('clé1', 100)
        """
        return self.__obtenir_paire__()

    def toString(self) -> str:
        """
        Retourne une chaîne de caractères représentant la paire clé-valeur.

        Retour :
        - str : Une représentation sous forme de chaîne de la paire.

        Exemple :
        >>> paire = CleValeur("clé1", 100)
        >>> paire.toString()
        'CleValeur(cle=clé1, valeur=100)'
        """
        return f"CleValeur(cle={self.cle}, valeur={self.valeur})"
ObjectId = str
"""
ObjectId est un alias pour le type str, utilisé pour représenter une identification unique sous forme de chaîne de caractères.

Description de l'élément :
Représente une chaîne de texte utilisée comme identifiant unique, souvent utilisée dans les bases de données.

Utilisation de l'élément :
Utilisez ObjectId pour typer les identifiants uniques en tant que chaînes dans votre programme.

Type de retour de l'élément :
- str : Représente une chaîne de caractères.

Exemple de l'élément :
user_id: ObjectId = "507f1f77bcf86cd799439011"
"""
Fonction = Callable[..., Any]
"""
Type générique représentant une fonction avec des paramètres variables et un retour quelconque.

Description de l'élément :
Représente une fonction Python pouvant accepter n'importe quel nombre et type de paramètres, et retournant un résultat quelconque.

Utilisation de l'élément :
Utilisez FunctionGeneric pour typer des fonctions qui acceptent une variété de paramètres sans spécification stricte de types.

Type de retour de l'élément :
- Callable[..., Any] : Une fonction Python générique.

Exemple de l'élément :
def exemple(*args: Any) -> Any:
    return args[0] if args else None
fonction: FunctionGeneric = exemple
"""
Object = dict
"""
Type représentant un dictionnaire Python générique.

Description de l'élément :
Représente un dictionnaire où les clés sont des chaînes de caractères et les valeurs peuvent être de tout type.

Utilisation de l'élément :
Utilisez ObjectGeneric pour typer des dictionnaires dont les valeurs ne sont pas contraignantes.

Type de retour de l'élément :
- dict : Un dictionnaire Python.

Exemple de l'élément :
obj: ObjectGeneric = {"clé": "valeur", "nombre": 42}
"""
ObjectWithNoFn = Dict[str, Any]
"""
Type représentant un dictionnaire dont les valeurs ne doivent pas être des fonctions.

Description de l'élément :
Représente un dictionnaire où les valeurs ne sont pas des fonctions, bien que Python ne permette pas de restreindre directement cela.

Utilisation de l'élément :
Utilisez ObjectWithNoFn pour typer des dictionnaires en veillant à ce que les valeurs ne soient pas des fonctions.

Type de retour de l'élément :
- Dict[str, Any] : Un dictionnaire Python avec des restrictions informelles sur les valeurs.

Exemple de l'élément :
obj: ObjectWithNoFn = {"clé": 42, "texte": "valeur"}
"""
MaybeArray = Union[T, List[T]]
"""
Type générique pouvant être une valeur unique ou une liste de valeurs.

Description de l'élément :
Peut représenter une valeur unique de type T ou une liste de valeurs du même type.

Utilisation de l'élément :
Utilisez MaybeArray lorsque vous avez besoin de gérer à la fois des valeurs uniques et des listes de valeurs.

Type de retour de l'élément :
- Union[T, List[T]] : Une seule valeur T ou une liste de valeurs T.

Exemple de l'élément :
single_value: MaybeArray[int] = 42
multiple_values: MaybeArray[int] = [1, 2, 3]
"""
Resultat = Union[T, asyncio.Future]
"""
Type générique pouvant être une valeur ou un futur résultat asynchrone.

Description de l'élément :
Permet de représenter un résultat qui peut être soit directement disponible soit produit de manière asynchrone.

Utilisation de l'élément :
Utilisez MaybePromise lorsque vous avez besoin de gérer des valeurs qui peuvent être retournées immédiatement ou après un traitement asynchrone.

Type de retour de l'élément :
- Union[T, asyncio.Future] : Une valeur T ou un futur asyncio contenant T.

Exemple de l'élément :
valeur: MaybePromise[int] = 42
futur: MaybePromise[int] = asyncio.Future()
"""

__all__=[
    CleValeur,
    ObjectId,
    Fonction,
    Object,
    ObjectWithNoFn,
    MaybeArray,
    NotFunction,
    is_not_function,
    AsType,
    AsString,
    Complete,
    Override,
    RecursivePartial,
    ArrayOneOrMore,
    RecursiveObjValueType,
    TypeObjectValues,
    NoExtraProperties,
    MakeObjKeysAsNever,
    RemoveTypeFromTuple,
    GetTypeKeyFromObject,
    RemoveTypeFromObj,
    GetObjectKeysThatAreOfType,
    ForceStringKeyObject,
    Indices,
    Writeable,
    DeepWriteable,
    IsObject,
    ReadonlyDeep,
    Exclusive,
    StringAndUnion,
    ArrayKeys,
    combine,
    keys,
    map_types,
    modify_mapping,
    remap_keys,
    template_literal,
    partial_dict,
    require_keys,
    create_record,
    omit_keys,
    exclude_members,
    extract_types,
    no_infer,
    typeOf,
    keyOf
]