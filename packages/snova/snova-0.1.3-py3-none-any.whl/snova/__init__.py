# you shouldn't be sneaking around these parts :p
from pathlib import Path
from random import choice
import aiohttp
import asyncio
import json

def to_lmc(content: str, role: str = "assistant") -> dict: 
    return {"role": role, "content": content}

def available() -> set:
    return {"Meta-Llama-3.1-8B-Instruct", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct", "Samba CoE", "Mistral-T5-7B-v1", "v1olet_merged_dpo_7B", "WestLake-7B-v2-laser-truthy-dpo", "DonutLM-v1", "SambaLingo Arabic", "SambaLingo Bulgarian", "SambaLingo Hungarian", "SambaLingo Russian", "SambaLingo Serbian (Cyrillic)", "SambaLingo Slovenian", "SambaLingo Thai", "SambaLingo Turkish", "SambaLingo Japanese"}

class SnSdk:
    def __init__(self, 
                 model="Meta-Llama-3.1-405B-Instruct", 
                 messages=None,
                 system="You are a helpful assistant.",
                 priority=0,
                 remember=False,
                 limit=30,
                 access_token="",
                 endpoint= "https://cloud.sambanova.ai/api/completion"):
    
        if model in available(): 
            self.model = model
        else: 
            self.model = "Meta-Llama-3.1-405B-Instruct"
        
        src = Path(Path(__file__).parent, "src")
        with open(Path(src, "user_agents.txt"), "r") as f:
            self.user_agent = choice(f.read().split("\n"))
            
        with open(Path(src, "mask_lmc.json"), "r") as f:
            self.mask = json.loads(f.read())
            
        with open(Path(src, "headers.json"), "r") as f:
            self.headers = json.loads(f.read())
            self.headers["User-Agent"] = self.user_agent
            self.headers["Priority"] = "u=" + str(priority)
            
        with open(Path(src, "body.json"), "r") as f:
            self.template = json.loads(f.read())
            self.template["body"]["model"] = self.model
        
        self.access_tokens = [access_token]
        if not access_token:
            with open(Path(src, "access_tokens.txt"), "r") as f:
                self.access_tokens = tuple(f.read().split("\n"))

        self.access_token = choice(self.access_tokens)
        self.messages = [] if messages is None else messages
        self.remember = remember
        self.limit = limit
        self.system = to_lmc(system, role="system")
        self.endpoint = endpoint
        
        self.loop = asyncio.get_event_loop()

    def mask_lmc(self, lmc: dict, i) -> dict:
        return lmc | self.mask | {"id": f"{(i//2)+1}-id", "ref": f"{(i//2)+1}-ref"}
            
    async def _stream_chat(self, data, remember=False):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, headers=self.headers, json=data, cookies={ "access_token": self.access_token}) as response:
                message, meta = "", {}
                async for line in response.content:
                    if line:
                        decoded_line = line.decode('utf-8')[6:]
                        if not decoded_line or decoded_line.strip() == "[DONE]":
                            continue

                        try:
                            json_line = json.loads(decoded_line)
                        except json.JSONDecodeError as e:
                            raise json.JSONDecodeError(e) # better implementation for later
                        
                        if not json_line.get("choices"):
                            meta = json_line
                            continue

                        options = json_line.get("choices")[0]
                        if options.get("finish_reason") == "end_of_text":
                            continue

                        chunk = options.get('delta', {}).get('content', '')
                        if self.remember or remember:
                            message += chunk
                        yield chunk
                
                if self.remember or remember:
                    self.messages.append(to_lmc(message) | meta)
                    if (length := len(self.messages)) > self.limit:
                        self.messages = self.messages[length-self.limit:]

    def chat(self, 
             message: str, 
             role="user", 
             stream=False,
             max_tokens=1400,
             remember=False, 
             lmc=False,
             system: str = None):
        
        system = to_lmc(system, role="system") if system else self.system
        if not lmc:
            message = to_lmc(message, role=role)
        elif message is None:
            message = self.messages[-1]
            self.messages = self.messages[:-1]
                    
        self.template["body"]["messages"] = [system] + [self.mask_lmc(i, j) for j, i in enumerate(self.messages)] + [self.mask_lmc(message, len(self.messages))]
        self.template["body"]["max_tokens"] = max_tokens
            
        if self.remember or remember:
            self.messages.append(message)
            
        if stream: 
            return self._stream_chat(self.template, remember)
        return self.loop.run_until_complete(self._static_chat(self.template, remember))
        
    async def _static_chat(self, template, remember):
        return "".join([chunk 
                        async for chunk in 
                        self._stream_chat(template, remember)])

async def main():
    llm = SnSdk()
    async for chunk in llm.chat(input("message: "), stream=True):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
