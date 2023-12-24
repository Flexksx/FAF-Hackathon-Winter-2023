from utils import *


class Selector:
    def __init__(self):
        self.__db = Database()

    def __custom_round(self, value):
        if np.isnan(value):
            return 0
        elif value == 0.9375:
            return 1.0
        elif value == 0.46875:
            return 0.5
        elif value == 1.40625:
            return 1.5
        elif value == 1.875:
            return 2
        elif value == 1.125:
            # Handle the case of 1.125 according to your requirements
            # For example, you can round it to 1 or 1.5 based on your preference
            return 1.5
        else:
            # For other values, you can use the default rounding behavior
            return round(value)

    def __apply_subject_round(self, df):
        df["theory"] = (df["theory"]/32).apply(self.__custom_round)
        df["seminar"] = (df["seminar"]/32).apply(self.__custom_round)
        df["lab"] = (df["lab"]/32).apply(self.__custom_round)
        df["project"] = (df["project"]/32).apply(self.__custom_round)
        return df

    def get_group_dfs(self, groupname: str, semester:int) -> tuple:
        """Extracts the needed dataframes for a single group

        Args:
            groupname (str): The name of the group

        Returns:
            tuple: A tuple containing the needed dataframes
        """
        teachers_df = self.__db.extract.teachers()
        groups_df = self.__db.extract.groups()
        subjects_df = self.__db.extract.subjects()

        subjects_df = self.__apply_subject_round(subjects_df)

        student_group_df = groups_df.loc[groups_df["name"] == groupname]
        gr_sub_map_df = self.__db.extract.group_subjects_maptable()
        gr_sub_map_df = gr_sub_map_df.loc[gr_sub_map_df["group_id"]
                                          == student_group_df["id"].values[0]]
        subject_ids = gr_sub_map_df["subject_id"]
        subjects_df = subjects_df.loc[(subjects_df["id"].isin(
            subject_ids)) & (subjects_df["semester"] == semester)]

        teachers_df = teachers_df.loc[teachers_df["id"].isin(
            subjects_df["id"].values)]

        return subjects_df, teachers_df, student_group_df

    def get_groups_dfs(self, groupnames: list,semester:list) -> dict:
        """Get dataframes for multiple groups in form of a dictionary containing pandas DataFrames

        Args:
            groupnames (list): List of group names that need to be extracted

        Returns:
            dict: A dictionary containing tuples with the needed dataframes
        """
        if len(groupnames) != len(semester):
            raise Exception("The number of groups and semesters must be equal")
        groups_dfs = {groupname : {"subjects":None,"teachers":None,"group":None} for groupname in groupnames}
        for i in range(len(groupnames)):
            subjects_df, teachers_df, student_group_df = self.get_group_dfs(
                groupnames[i],semester[i])
            groups_dfs[groupnames[i]]["subjects"]=subjects_df
            groups_dfs[groupnames[i]]["teachers"]=teachers_df
            groups_dfs[groupnames[i]]["group"]=student_group_df
        return groups_dfs
