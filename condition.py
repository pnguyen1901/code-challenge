import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Agent:
  def __init__(self, voicemail):
    self.voicemail = voicemail

  def __repr__(self):
    return ('''
      voicemail: {}
    ''').format(self.voicemail)

def consumer(agent, condition):
    with condition:
        logging.debug('waiting to return customer call')
        condition.wait()
        logging.debug('returning customer call')
        agent.voicemail.pop(0)

def producer(agent, condition):
    logging.debug('acquiring lock. Agent is busy serving customer')
    with condition:
        time.sleep(2)
        logging.debug('Agent is available now')
        condition.notify()

if __name__ == '__main__':
    
    agents = [Agent([2,3]), Agent([1,5,3])]


    for _ in range(2):
      condition = threading.Condition()
      agent = agents[_]
      agent.voicemail.append(23)
      cs1 = threading.Thread(target=consumer, args=(agent, condition,))
      #cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
      pd1 = threading.Thread(target=producer, args=(agent, condition,))
      #pd2 = threading.Thread(name='producer2', target=producer, args=(condition,))

      cs1.start()
      time.sleep(2)
      #cs2.start()
      #time.sleep(2)
      pd1.start()
      cs1.join()
      pd1.join()
      #time.sleep(2)
      #pd2.start()

    # main_thread = threading.current_thread()
    # for t in threading.enumerate():
    #   if t is not main_thread:
    #     t.join()
    print(agents)