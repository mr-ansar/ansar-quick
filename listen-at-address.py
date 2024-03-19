import ansar.connect as ar

root = ar.startup(ar.log_to_stderr)

root.create(listen_at_address)
root.select(ar.Completed, ar.Stop)
ar.tear_down(exit_code=0)

def listen_at_address(self)
  ar.listen(self, HostPort())
  m = self.select(ar.Listening, ar.NotListening, ar.Stop)
  if not isinstance(m, ar.Listening):
    return
  while True:
    m = self.select(ar.Accepted, ar.Abandoned, ar.Closed, ar.Stop)
    if not isinstance(m, ar.Listening):
      return
    
    
    
    
