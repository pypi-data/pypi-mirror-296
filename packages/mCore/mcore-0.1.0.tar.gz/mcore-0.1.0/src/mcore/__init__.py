import sys
from .type import *
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__all__=[
    __version__,
    CleValeur,
    IdentifiantObjet,
    Fonction,
    Objet,
    ObjetSansFonction,
    PeutEtreTableau,
    NonFonction,
    est_non_fonction,
    CommeType,
    CommeChaine,
    Complet,
    Remplacer,
    PartielRécursif,
    TableauUnOuPlus,
    TypeValeurObjetRécursif,
    TypeValeurObjets,
    PasDeProprietesSupplementaires,
    FaireDesClesObjetsCommeJamais,
    SupprimerTypeDuTuple,
    ObtenirCleTypeDeObjet,
    SupprimerTypeDeObjet,
    ObtenirClesDeObjetDeType,
    ForcerObjetCleString,
    Indices,
    Ecrivable,
    EcrivableProfond,
    EstObjet,
    LectureSeuleProfonde,
    Exclusif,
    ChaineEtUnion,
    ClesTableau,
    combiner,
    cles,
    mapper_types,
    modifier_mappage,
    remapper_cles,
    modele_literal,
    dictionnaire_partiel,
    exiger_cles,
    creer_enregistrement,
    omettre_cles,
    exclure_membres,
    extraire_types,
    pas_inferer,
    typeDe,
    cleDe,
]