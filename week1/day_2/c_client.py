import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

class AsaanHTTPClient:
    def __init__(self, max_requests: int = 2):
        self.bouncer = asyncio.Semaphore(max_requests)
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=5.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=2.5),
        # Sirf network errors ya status errors par retry karein (DecodeError par nahi!)
        retry=retry_if_exception_type(httpx.HTTPError), 
        reraise=True 
    )
    async def _bhejo_request_with_retry(self, url: str):
        print(f"-> Internet par request bhej rahe hain: {url}")
        response = await self.client.get(url)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"❌ [HTTP Error]: {e} | Link: {url}")
            raise e
        try:
            return response.json()
        except Exception:
            return response.text

    async def get_data(self, url: str):
        async with self.bouncer:
            try:
                data = await self._bhejo_request_with_retry(url)
                return data
            except httpx.HTTPStatusError as e:
                print(f"❌ [Error] {e.response.status_code} | Link: {url}")
                return None
            except httpx.HTTPError as e:
                print(f"❌ [Network Error]: {e} | Link: {url}")
                return None

async def main():
    urls = [
        "https://httpbin.org/json",
        "https://httpbin.org/status/503",
        "https://httpbin.org/delay/1"
    ]
    all_results = []
    batch_size = 2
    print("=== Program Shuru Ho Raha Hai ===")
    async with AsaanHTTPClient(max_requests=2) as smart_client:
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i : i + batch_size]
            tasks = [smart_client.get_data(url) for url in batch_urls]
            results = await asyncio.gather(*tasks)
            all_results.extend(results)
            await asyncio.sleep(0.5) #rest after each batch
        
        print("\n=== Final Results Summary ===")
        for index, result in enumerate(all_results):
            status = "Kamyab (Data Mil Gaya)" if result else "Nakaam (None mila)"
            print(f"Link {index + 1}: {status}")

asyncio.run(main())