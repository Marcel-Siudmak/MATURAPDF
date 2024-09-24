from PyPDF2 import PdfReader, PdfWriter
from maturaTasksViewer import find_tasks_in_pdf

class Matura:
    def __init__(self, path:str):
        self.path = path
        
    def createTask(self, task=False):
        self.writer = PdfWriter()
        self.reader = PdfReader(self.path)
        def addPage(self, pg:int, up:int=None, bottom:int=None):
            page = self.reader.pages[pg]
            height = page.mediabox.height

            if up!=None and bottom!=None:
                page.mediabox.top = (height-up)
                page.mediabox.bottom = (height-bottom)
            elif up!=None:
                page.mediabox.top = (height-up)
                page.mediabox.bottom = (60)
            elif bottom!=None:
                page.mediabox.bottom = (height-bottom)
            else:
                page.mediabox.bottom = (60)
            
            self.writer.add_page(page)

        def save(self, path:str):
            with open(path, "wb") as fp:
                self.writer.write(fp)
            self.writer.close()

        
        if type(task)==type({}):
            number, name, pstart, pend, up, bottom = list(task.values())
        else:
            number, name, pstart, pend, up, bottom = task
        up, bottom = int(up), int(bottom)
        print(number, name, pstart, pend, up, bottom)

        

        if pstart==pend:
            addPage(self, pstart, up, bottom)
        else:
            for i in range(pstart, pend+1):
                if i==pstart:
                    addPage(self, i, up=up)
                elif i==pend:
                    addPage(self, i, bottom=bottom)
                else:
                    addPage(self, i)
            
        save(self, "./tasks/"+number+name+".pdf")

    def autoCreator(self):
        tasklist=[]
        for task in find_tasks_in_pdf(self.path):
            task=list(task.values())
            self.createTask(task)

matura = Matura("test.pdf")
matura.autoCreator()

# tasklist=[]
# for task in find_tasks_in_pdf("test.pdf"):
#     task=list(task.values())
#     matura.createTask(task)