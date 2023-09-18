import aiofiles
from queue import Queue


class CycleQueue:
    # Queue to save in json file

    def __init__(self, data):
        self.queue = Queue()
        self._data = data

    def pool_queue(self):
        self.queue.put(self._data)

    def run_queue(self):
        # pipe run command shell
        self.pool_queue()
        task = self.queue.get()  # queue tasks
        if task:
            if not hasattr(self, '_label'):
                self._label = task
                yield self._label
        # stored datas
        self._to_save(self._label)

    async def _to_save(self, data):
        with aiofiles.open('output_prompt.jsonl', "a+") as _json:
            await _json.write("%s\n" % data)


if __name__ == '__main__':
    cycle = CycleQueue('netstat -a')
    out_flow = cycle.run_queue()
    print("".join(map(str, out_flow)))
