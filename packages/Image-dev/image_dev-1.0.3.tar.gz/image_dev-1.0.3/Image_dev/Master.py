from .ExcuteThread import ExcuteThread
from .ExcuteAmphenol import ExcuteAmphenol
from .ExtractImageName import unifyImageName, extractImageName
from os import makedirs

class runAll():
    def __init__(self, df, output_path, down_path, exclude_path, Amphenol):

        self.df= df
        self.output_path=output_path
        self.down_path=down_path
        self.exclude_path= exclude_path

        self.which_run= lambda urls_and_names:  ExcuteAmphenol(urls_and_names, output_path, down_path, exclude_path) \
                                                if Amphenol else ExcuteThread(urls_and_names, output_path, down_path, exclude_path)
        #Set Image Names
        dict_image_names= {url:name 
                           for url, name in 
                           zip(self.df['Original_Image_UP'].drop_duplicates(),
                                unifyImageName(
                                    self.df['Original_Image_UP'].drop_duplicates().apply(extractImageName))) }
        self.df['Image_Name']= self.df['Original_Image_UP'].map(dict_image_names)
        print('Image Name Set Successfully.')
        #create foler
        self.createFolders()
        self.Excute(self.df)
        self.setPathes()
        
    def Excute(self, temp_df):
        results = self.which_run(zip(temp_df['Original_Image_UP'], temp_df['Image_Name'])).getResults()
        self.df['Status']= self.df['Image_Name'].map({k: v[0] for k, v in results.items()})
        self.df['HashCode']= self.df['Image_Name'].map({k: v[1] for k, v in results.items()})
        print('Download And Reszie Done.')
    def setPathes(self):
        self.df['L']= self.df['Image_Name'][self.df['Status']=='DONE'].apply(lambda x: rf"{self.output_path}\Large\{x}.jpg")
        self.df['S']= self.df['Image_Name'][self.df['Status']=='DONE'].apply(lambda x: rf"{self.output_path}\Small\{x}.jpg")
        self.df['O']= self.df['Image_Name'][self.df['Status']=='DONE'].apply(lambda x: rf"{self.output_path}\Orignal\{x}.jpg")
        self.df['OR']= self.df['Image_Name'][self.df['Status']=='DONE'].apply(lambda x: rf"{self.down_path}\{x}.jpg")

    def createFolders(self):
        makedirs(self.output_path)
        makedirs(rf"{self.output_path}\Small")
        makedirs(rf"{self.output_path}\Large")
        makedirs(rf"{self.output_path}\Orignal")
    

