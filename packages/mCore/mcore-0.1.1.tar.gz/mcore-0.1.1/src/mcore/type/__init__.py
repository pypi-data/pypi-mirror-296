import sys


from .generic import CleValeur as CleValeur, ObjectId as IdentifiantObjet, Fonction as Fonction, Object as Objet, ObjectWithNoFn as ObjetSansFonction, MaybeArray as PeutEtreTableau, NotFunction as NonFonction, is_not_function as est_non_fonction, AsType as CommeType, AsString as CommeChaine, Complete as Complet, Override as Remplacer, RecursivePartial as PartielRécursif, ArrayOneOrMore as TableauUnOuPlus, RecursiveObjValueType as TypeValeurObjetRécursif, TypeObjectValues as TypeValeurObjets, NoExtraProperties as PasDeProprietesSupplementaires, MakeObjKeysAsNever as FaireDesClesObjetsCommeJamais, RemoveTypeFromTuple as SupprimerTypeDuTuple, GetTypeKeyFromObject as ObtenirCleTypeDeObjet, RemoveTypeFromObj as SupprimerTypeDeObjet, GetObjectKeysThatAreOfType as ObtenirClesDeObjetDeType, ForceStringKeyObject as ForcerObjetCleString, Indices as Indices, Writeable as Ecrivable, DeepWriteable as EcrivableProfond, IsObject as EstObjet, ReadonlyDeep as LectureSeuleProfonde, Exclusive as Exclusif, StringAndUnion as ChaineEtUnion, ArrayKeys as ClesTableau, combine as combiner, keys as cles, map_types as mapper_types, modify_mapping as modifier_mappage, remap_keys as remapper_cles, template_literal as modele_literal, partial_dict as dictionnaire_partiel, require_keys as exiger_cles, create_record as creer_enregistrement, omit_keys as omettre_cles, exclude_members as exclure_membres, extract_types as extraire_types, no_infer as pas_inferer, typeOf as typeDe, keyOf as cleDe

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