import json,os,sys,time
LOG_LEVEL=os.getenv("LOG_LEVEL","INFO")
class JSONLogger:
    LEVELS={"DEBUG":10,"INFO":20,"WARN":30,"ERROR":40}
    def __init__(self,level=LOG_LEVEL): self.level=self.LEVELS.get(level.upper(),20)
    def _log(self,level,msg,**kwargs):
        if self.LEVELS[level]<self.level: return
        record={"ts":time.time(),"level":level,"message":msg,**kwargs}
        sys.stdout.write(json.dumps(record)+"\n"); sys.stdout.flush()
    def debug(self,msg,**kw): self._log("DEBUG",msg,**kw)
    def info(self,msg,**kw): self._log("INFO",msg,**kw)
    def warn(self,msg,**kw): self._log("WARN",msg,**kw)
    def error(self,msg,**kw): self._log("ERROR",msg,**kw)
logger=JSONLogger()
