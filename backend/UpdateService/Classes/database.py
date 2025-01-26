from sqlmodel import Session, select
from typing import List
import json
from Models.model import *

class OperationDB:
    """
        Classe de fonctions pour travailler avec la base de données
    """

    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()

    """
        Fonctions de contrôle d'existence
        En cas de succès, renvoie le premier des objets trouvés
        En cas d'échec, aucun
    """
    def check_event_existence(self, event: Event):
        filters = {key: value for key, value in event.model_dump(exclude={"id", "location", "teacher", "year", "group", "subgroup"}).items() if value is not None}
        query = select(Event).filter_by(**filters)
        result = self.session.exec(query)
        return result.first()

    def check_event_existence_hash(self, event_hash:str):
        query = select(Event).where(Event.hash == event_hash)
        result = self.session.exec(query)
        return result.first()

    def check_location_existence(self, location: Location):
        query = select(Location).filter_by(name=location.name)
        result = self.session.exec(query)
        return result.first()

    def check_teacher_existence(self, teacher: Teacher):
        query = select(Teacher).filter_by(name=teacher.name)
        result = self.session.exec(query)
        return result.first()

    def check_group_existence(self, group: GroupTree):
        query = select(GroupTree).filter_by(name=group.name)
        result = self.session.exec(query)
        return result.first()

    """
        Fonctions de création de nouveaux objets dans la base de données
        Dans le cas de la recherche d'objets existants, vérification de la présence de tous les attributs
    """

    def create_event(self, event: Event):
        dataBaseRec = self.check_event_existence(event)
        if  dataBaseRec is None:
            print("Sur le point d'ajouter ", event.model_dump())
            self.session.add(event)
        else:
            print("\nAjout de champs ", event.model_dump())
            # dataBaseRec.add(event)

    def create_group(self, group: GroupTree):
        dataBaseRec = self.check_group_existence(group)
        if dataBaseRec is None:
            self.session.add(group)
            return self.check_group_existence(group)
        return dataBaseRec

    def create_location(self, location: Location):
        dataBaseRec = self.check_location_existence(location)
        if dataBaseRec is None:
            self.session.add(location)
            return self.check_location_existence(location)
        return dataBaseRec

    def create_teacher(self, teacher: Teacher):
        dataBaseRec = self.check_teacher_existence(teacher)
        if dataBaseRec is None:
            self.session.add(teacher)
            return self.check_teacher_existence(teacher)
        return dataBaseRec

    # ajouter la possibilité de changer le nom en un nom équivalent et de l'ajouter à la liste (dictionnaire)
    # d'autres exceptions à vérifier lors de l'utilisation de la base de données pour les nouveaux cas décrits
    # le système devrait être plus global car l'erreur vient des fichiers de mise à jour (peut-on faire quelque chose à ce sujet ? ??)
    # par essence, nous avons un seul json, nous pouvons donc probablement
    @staticmethod
    def writeToJson(table, copy, original):
        with open("exceptions.json", "w") as file:
            data = json.load(file)
            data[table][copy] = original
            json.dump(data, file, indent=4)

    def makeEquivalentLocation(self, locationOriginal: Location, locationCopy: Location):
        locationOriginal = self.check_location_existence(locationOriginal)
        locationCopy = self.check_location_existence(locationCopy)
        if locationOriginal is None or locationCopy is None:
            return "Location doesn't exist"
        locationOriginal.events.extend(locationCopy.events)
        copyName = locationCopy.name
        self.session.delete(locationCopy)
        OperationDB.writeToJson("locations", copyName, locationOriginal.name)

    def makeEquivalentTeacher(self, teacherOriginal: Teacher, teacherCopy: Teacher):
        teacherOriginal = self.check_teacher_existence(teacherOriginal)
        teacherCopy = self.check_teacher_existence(teacherCopy)
        if teacherOriginal is None or teacherCopy is None:
            return "Teacher doesn't exist"
        teacherOriginal.events.extend(teacherCopy.events)
        copyName = teacherCopy.name
        self.session.delete(teacherCopy)
        OperationDB.writeToJson("teachers", copyName, teacherOriginal.name)

    def makeEquivalentGroup(self, groupOriginal: GroupTree, groupCopy: GroupTree):
        groupOriginal = self.check_group_existence(groupOriginal)
        groupCopy = self.check_group_existence(groupCopy)
        if groupOriginal is None or groupCopy is None:
            return "Group doesn't exist"
        groupOriginal.events.extend(groupCopy.events)
        copyName = groupCopy.name
        self.session.delete(groupCopy)
        OperationDB.writeToJson("groups", copyName, groupOriginal.name)

    def changeLevel(self, child: List[str], parent: str):
        parent = self.session.exec(select(GroupTree).where(GroupTree.name==parent)).first()
        if not parent is None:
            items = self.session.exec(select(GroupTree).where(GroupTree.name.in_(child))).all()
            for item in items:
                item.parent_id = parent.id


    # def putToNextLevel(self, child: List[GroupTree], parent: GroupTree):
    #     parent = self.check_group_existence(parent)
    #     if  parent is None:
    #         return "Parent doesn't exist"
    #     for group in child:
    #         gr = self.check_group_existence(group)
    #         if not gr is None:
    #             gr.parent_id = parent.id
    #     return

    def imageRec(self, currentLevelElls: List[GroupTree] = None, level = 0):
        if level == 0:
            currentLevelElls = self.session.exec(select(GroupTree).where(GroupTree.parent_id == None)).all()
        for ell in currentLevelElls:
            print(" |"* level, end="")
            print(f"-{ell.name}, id: {ell.id}")
            query = select(GroupTree).where(GroupTree.parent_id == ell.id)
            result = self.session.exec(query).all()
            self.imageRec(result, level+1)

    """
        Suppression des index obsolètes
    """

    def deleteObsoleteIndexes(self, lastDetectionIndex):
        print("\n\nÉTAPE DE DÉMONTAGE")
        query = select(Event).where(Event.last_detection != lastDetectionIndex)
        results = self.session.exec(query)
        for result in results:
            print("Supprimé: " + result.model_dump())
            self.session.delete(result)
