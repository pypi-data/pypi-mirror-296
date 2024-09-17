import os, json
import requests
from .unitypredictUtils import ReturnValues as Ret
from .UnityPredictLocalHost import UnityPredictHost

class UnityPredictCli:
    def __init__(self) -> None:

        self._uptCredFolder = ".unitypredict"
        self._uptCredFile = "credentials"
        self._userRoot = os.path.expanduser("~")
        self._uptCredDir = os.path.join(self._userRoot, self._uptCredFolder)
        self._uptCredPath = os.path.join(self._uptCredDir, self._uptCredFile)

        # self._uptEntryPointAPI = "https://api.dev.unitypredict.net/api/engines/supportedengines"
        self._uptEntryPointAPI = "https://api.prod.unitypredict.com/api/engines/supportedengines"
        self._uptEntryPointFieName = "EntryPoint.py"
        
        # Get API key
        self._uptApiKey = {}
        if os.path.exists(self._uptCredPath):
            with open(self._uptCredPath) as credFile:
                self._uptApiKey = json.load(credFile)
            

        

    def configureCredentials(self, uptApiKey: str| None):

        if not os.path.exists(self._uptCredDir):

            os.mkdir(self._uptCredDir)
            
        self._uptApiKey = {"UPT_API_KEY": uptApiKey}
        
        try:
            with open(self._uptCredPath, "w+") as credFile:
                credFile.write(json.dumps(self._uptApiKey, indent=4))
        except Exception as e:
            print (f"Error in creating file {self._uptCredPath}: {e}")
            return Ret.CRED_CREATE_ERROR
        
        return Ret.CRED_CREATE_SUCCESS
    
    def showCredentials(self):
        
        print(f"{json.dumps(self._uptApiKey, indent=4)}")

    
    def createEngine(self):
        apiKey = self._uptApiKey["UPT_API_KEY"]
        print ("Creating Engine Components ...")
        initEngine = UnityPredictHost(apiKey=apiKey)
        if not initEngine.isConfigInitialized():
            print ("Engine Components creation Failed!!")
            return Ret.ENGINE_CREATE_ERROR

        print ("Engine Components creation Success!!")
        # Fetch the entrypoint details
        print ("Fetching EntryPoint.py template ...")
        headers = {"Authorization": f"Bearer {apiKey}"}
        response = requests.get(self._uptEntryPointAPI, headers=headers)
        if response.status_code != 200:
            print (f"EntryPoint.py template fetch Failure with error code: {response.status_code}")
            print(response.text)
            return Ret.ENGINE_CREATE_ERROR
        
        try:
            suppPlatforms = response.json()
            for suppPlatform in suppPlatforms:
                if suppPlatform["platformKey"] != "SL_CPU_BASE_PYTHON_3.12":
                    continue

                entrypointResp = requests.get(suppPlatform["entryPointTemplateUrl"])
                if entrypointResp.status_code != 200:
                    print (f"EntryPoint.py template fetch Failure with error code: {entrypointResp.status_code}")
                    print(entrypointResp.text)
                    return Ret.ENGINE_CREATE_ERROR
                

                entrypointContent = entrypointResp.text
                entryPointFile = os.path.join(os.getcwd(), self._uptEntryPointFieName)

                with open(entryPointFile, "w+")as efile:
                    efile.write(entrypointContent)

                break

        except Exception as e:
            print (f"Exception Occured while fetching EntryPoint: {e}")
            return Ret.ENGINE_CREATE_ERROR


        print ("EntryPoint.py template fetch Success!!")
        
        return Ret.ENGINE_CREATE_SUCCESS

