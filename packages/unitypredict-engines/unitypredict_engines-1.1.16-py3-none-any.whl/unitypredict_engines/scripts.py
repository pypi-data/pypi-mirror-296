import sys, os, shutil
from .unitypredictcli import UnityPredictCli
from .unitypredictUtils import ReturnValues as Ret
import argparse

def main():
    cliExec = "UnityPredict SDK"
    parser = argparse.ArgumentParser(
            description="Welcome to {}".format(cliExec)
    )
   
    parser.add_argument("--config_cred", action="store_true", help=f"configure the credentials of {cliExec}")
    parser.add_argument("--show_cred", action="store_true", help=f"show credentials configured for {cliExec}")
    parser.add_argument("-ce", "--create_engine", action="store_true", help=f"create AppEngine template using {cliExec}")
    parser.add_argument("-ename", "--engine_name", default="firstEngine", help="""set the AppEngine name. 
                                                                            Used after the [-ce][--create_engine]""")
    # parser.add_argument("-key", "--apiKey", default=None, help=f"Used to add api key of the users unityPredict account.
    #                                                             Used after the [-ce][--create_engine], if [--config_cred] not executed")

    args = parser.parse_args()

    num_args = len(sys.argv) - 1
    
    if (num_args == 0):
        parser.print_help()
        sys.exit(0)

    cliDriver = UnityPredictCli()

    if args.config_cred:
        inputApiKey = input("Enter your UnityPredict account API Key: ")
        inputApiKey = inputApiKey.strip()
        ret = cliDriver.configureCredentials(uptApiKey=inputApiKey)
        if ret == Ret.CRED_CREATE_SUCCESS:
            cliDriver.showCredentials()
        sys.exit(0)

    if args.show_cred:
        cliDriver.showCredentials()
        sys.exit(0)

    if args.create_engine:
        currPath = os.getcwd()
        enginePath = os.path.join(currPath, args.engine_name)
        if os.path.exists(enginePath):
            print ("""The engine already exists on the current directory. You can:
                   - Change the directory
                   - Use --engine_name flag to change the name of the engine
                   """)
            sys.exit(0)
        os.mkdir(enginePath)
        os.chdir(enginePath)
        ret = cliDriver.createEngine()
        os.chdir(currPath)
        if ret == Ret.ENGINE_CREATE_ERROR:
            if os.path.exists(enginePath):
                print (f"Removing Engine {args.engine_name} due to Engine Creation errors!")
                shutil.rmtree(enginePath)
        sys.exit(0)
    


