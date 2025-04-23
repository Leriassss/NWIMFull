# This Python file uses the following encoding: utf-8

class FileManager:

    def readFile(self, filePath):
        try:
            if filePath.endswith('.csv'):
                df = pd.read_csv(filePath)
            elif filePath.endswith('.xlsx'):
                df = pd.read_excel(filePath, engine='openpyxl')
            else:
                print("Format de fichier non supporté")
                return

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
