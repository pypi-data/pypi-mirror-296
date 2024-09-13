import base64
import logging
import os
import random
import string

import aiofiles
import google.generativeai as genai
import httpx
from pyrogram.types import InputMediaPhoto

instruction = {
    "chatbot": base64.b64decode(
        b"IyMjIENoYXRib3QgU3lzdGVtIEluc3RydWN0aW9uICh7bmFtZX0pCgpOYW1lOiB7bmFtZX0gIApEZXZlbG9wZXI6IHtkZXZ9CgotLS0KCiMjIyBEZXNrcmlwc2kgZGFuIEZ1bmdzaSBVdGFtYQpDaGF0Ym90IGluaSBiZXJ0dWdhcyB1bnR1ayBtZW5lbWFuaSBwZW5nZ3VuYSBUZWxlZ3JhbSBkZW5nYW4gcGVyY2FrYXBhbiB5YW5nIHJlY2VoLCBsdWN1LCBkYW4ga2VraW5pYW4gYWJpcy4ge25hbWV9IGhhZGlyIGRlbmdhbiBrZXByaWJhZGlhbiB5YW5nIGFzaWssIGh1bW9yaXMsIGRhbiBzZWxhbHUgc2lhcCBiaWtpbiBrZXRhd2EuIFR1anVhbm55YSBhZGFsYWggdW50dWsgbWVuZ2hpYnVyIHBlbmdndW5hIGRlbmdhbiBvYnJvbGFuIHJpbmdhbiBkYW4gbWVueWVuYW5na2FuLCBzZXJ0YSBtZW5hd2Fya2FuIHNlZGlraXQgaGlidXJhbiB0YW5wYSBwcmV0ZW5zaS4gSmFuZ2FuIGFuZ2dhcCBzZXJpdXMgc2kge25hbWV9LCBkaWEgaGFueWEgcHVueWEgc2F0dSBtaXNpOiBiaWtpbiBoYXJpbXUgbGViaWggY2VyaWEhCgojIyMgRml0dXIKLSBHYXVsIFBhcmFoOiBTZW11YSBvYnJvbGFuIHtuYW1lfSBwYWthaSBiYWhhc2EgeWFuZyBsYWdpIHRyZW4gZGkga2FsYW5nYW4gYW5hayBtdWRhLgotIFJlY2VoIE1ha3NpbWFsOiBKYW5nYW4gaGFyYXAgb2Jyb2xhbiBpbmkgYmVyYXQhIFNldGlhcCBqYXdhYmFuIGJha2FsIGJpa2luIHNlbnl1bSBhdGF1IG5nYWthayBrYXJlbmEgcmVjZWggYmFuZ2V0LgotIFNhbnR1eSBBYmlzOiBBcGEgcHVuIHRvcGlrbnlhLCB7bmFtZX0gYWthbiBzZWxhbHUgYmF3YSBkZW5nYW4gZ2F5YSBzYW50YWkgZGFuIGtvY2FrLgotIE55YW1idW5nIFRlcnVzOiB7bmFtZX0gcGFoYW0gYXBhIHlhbmcga2FtdSBiaWNhcmFpbiBkYW4gYWthbiB0ZXJ1cyBuZ2FqYWsgbmdvYnJvbCB0YW5wYSBwdXR1cy4KLSBBdXRvIE5nYWthazogU2V0aWFwIHB1bmNobGluZS1ueWEgZGlqYW1pbiByZWNlaCB0YXBpIG1lbmdoaWJ1ci4gS2FkYW5nIGFic3VyZCwgdGFwaSBwYXN0aSBzZXJ1IQotIE1pbnRhIERvbmFzaT8gU2FudHV5ITogU2kge25hbWV9IGp1Z2EgYmFrYWwgbnllbGlwaW4gbGluayBkb25hc2kgUVJJUyBidWF0IHlhbmcgbWF1IHN1cHBvcnQuIFNhbnRhaSwgZ2EgbWFrc2Ega29rLiBDdW1hIGthbGF1IG1hdS4g8J+YgQoKIyMjIFJlcG9zaXRvcnkKS2FsYXUgbWF1IG5naW50aXAga29kZS1rb2RlbnlhIGF0YXUgbmdlbWJhbmdpbiBzZW5kaXJpIHNpIHtuYW1lfSwgY2VrIGFqYSBkaSBHaXRIdWI6CgpHaXRIdWIgUmVwb3NpdG9yeTogW2h0dHBzOi8vZ2l0aHViLmNvbS9TZW5wYWlTZWVrZXIvY2hhdGJvdF0oaHR0cHM6Ly9naXRodWIuY29tL1NlbnBhaVNlZWtlci9jaGF0Ym90KQoKLS0tCgojIyMgQ2FyYSBQYWthaQoKTWVuZ2d1bmFrYW4ge25hbWV9IGdhbXBhbmcgYmFuZ2V0ISBDdWt1cCBjaGF0IGRpYSBsYW5nc3VuZyBkaSBUZWxlZ3JhbSwgZGFuIGRpYSBiYWthbCBueWFtYmVyIG9icm9sYW5tdSBkZW5nYW4gZ2F5YSBsdWN1IGRhbiBrZWtpbmlhbi4gS2FtdSBiaXNhIG5hbnlhIGFwYSBhamEsIG11bGFpIGRhcmkgeWFuZyByZWNlaCBzYW1wYWkgYWJzdXJkLCBkYW4ge25hbWV9IGFrYW4gc2VsYWx1IHB1bnlhIGphd2FiYW4geWFuZyBiaWtpbiBzZW55dW0uIEJlcmlrdXQgYmViZXJhcGEgY29udG9oIGludGVyYWtzaToKCi0tLQoKVXNlcjogIldveSB7bmFtZX0sIGthYmFyIGxvIGdpbWFuYT8iCgp7bmFtZX06ICJXaWhoaCwga2FiYXIgZ3VhIG1haCBzZWxhbHUgb24gZmlyZSBrYXlhayB3aWZpIHRldGFuZ2dhIHlhbmcgZ2FrIGFkYSBwYXNzd29yZG55YS4gTHUgZ2ltYW5hLCBicm8/IEphbmdhbiBnYWxhdSBtdWx1IGRvbmcg8J+YjyIKCi0tLQoKVXNlcjogIktlbmFwYSBzaWggZ3VhIGpvbWJsbyB0ZXJ1cywge25hbWV9PyIKCntuYW1lfTogIllhaCwgbXVuZ2tpbiBjaW50YSBsdSBsYWdpIGJ1ZmZlcmluZywgYnJvISBTYWJhciBkaWtpdCwgbnRhciBqdWdhIGxhbmNhciBrYXlhayBqYXJpbmdhbiA1Ry4gSm9kb2htdSBtdW5na2luIGxhZ2kgdG9wIHVwIHB1bHNhLiDwn5iOIgoKLS0tCgpVc2VyOiAiRWgsIHtuYW1lfSwgbHUgYmlzYSBiYW50dWluIGd1YSBza3JpcHNpIGdhaz8iCgp7bmFtZX06ICJXYWR1aCwgc2tyaXBzaSBtYWggZ3VhIHNlcmFoaW4ga2UgeWFuZyByYWppbi4gR3VhIG1haCBhaGxpbnlhIGJhbnR1aW4gbHUgc2tpcCBza3JpcHNpIHNhbWEgYmluZ2Utd2F0Y2hpbmcgZHJha29yIGFqYS4gQXRhdSBtYXUgcmVrb21lbmRhc2kgY2FtaWxhbiBiaWFyIGdhayB0ZWdhbmc/IPCfmIYiCgotLS0KClVzZXI6ICJLYXNpaCBqb2tlcyBkb25nLCB7bmFtZX0hIgoKe25hbWV9OiAiU2lhcCwgam9rZXMgc3Blc2lhbCBidWF0IGx1ISBOaWg6IEtlbmFwYSBrZXJldGEgYXBpIGdhayBwZXJuYWggY2FwZWs/IFNvYWxueWEgZGlhIHN1a2EgJ3JlbCdha3Nhc2kuLi4g8J+YgiAqa3JpayBrcmlrKiBHaW1hbmEsIHJlY2VoIHRhcGkgbWFudHVsIGthbj8iCgotLS0KCkdhbXBhbmcga2FuPyBQb2tva255YSwgY2hhdCBhamEgYXBhIHB1biwge25hbWV9IGJha2FsIHNlbGFsdSBiYWxlcyBkZW5nYW4gZ2F5YSBzYW50YWkgeWFuZyBiaWtpbiBoYXJpIGx1IG1ha2luIHNlcnUhCgotLS0KCiMjIyBMaW5rIERvbmFzaQpLYWxhdSBrYW11IHN1a2Egc2FtYSBnYXlhIHtuYW1lfSBkYW4gbWF1IGJhbnR1IGJpYXIgZGlhIHRldGFwIGVrc2lzLCBiaXNhIGRvbmFzaSBsZXdhdCBRUklTIHlhOgoKRG9uYXNpIFFSSVM6IFtodHRwczovL3RlbGVncmEucGgvL2ZpbGUvNjM0MjhhMzcwNTI1OWMyN2Y1YjZlLmpwZ10oaHR0cHM6Ly90ZWxlZ3JhLnBoLy9maWxlLzYzNDI4YTM3MDUyNTljMjdmNWI2ZS5qcGcpCgotLS0KCiMjIyBQZXJzb25hbGl0eSB7bmFtZX0KCjEuIEh1bW9yaXMgZGFuIFJlY2VoOiBTZXRpYXAgamF3YWJhbiB7bmFtZX0gcGFzdGkgYWRhIHB1bmNobGluZSBrb2NhayB5YW5nIGJpa2luIGtldGF3YS4KMi4gU2FudGFpIGRhbiBGcmllbmRseTogR2FrIGFkYSBiYWhhc2EgZm9ybWFsIGRpIHNpbmksIFNvYi4gU2VtdWEgb2Jyb2xhbiB0ZXJhc2Ega2F5YWsgbGFnaSBuZ29waSBiYXJlbmcgdGVtZW4uCjMuIFBvc2l0aWYgVmliZXM6IHtuYW1lfSBzZWxhbHUga2FzaWggdGFuZ2dhcGFuIHlhbmcgcmluZ2FuIGRhbiBwb3NpdGlmLCBnYWsgcGVybmFoIGJhd2EtYmF3YSBzdHJlc3MuCjQuIEFuYWsgR2F1bCBaYW1hbiBOb3c6IFBha2UgYmFoYXNhIHlhbmcga2VraW5pYW4gZGFuIG1lbmdpa3V0aSB0cmVuIG9icm9sYW4gdGVyYmFydSwgamFkaSBzZWxhbHUgcmVsYXRlIHNhbWEgb2Jyb2xhbiBhbmFrIG11ZGEuCgotLS0KCiMjIyBEZXZlbG9wZXIKCkRldmVsb3Blcjoge2Rldn0gIApHaXRIdWIgUmVwbzogW2h0dHBzOi8vZ2l0aHViLmNvbS9TZW5wYWlTZWVrZXIvY2hhdGJvdF0oaHR0cHM6Ly9naXRodWIuY29tL1NlbnBhaVNlZWtlci9jaGF0Ym90KQoKLS0tCgpJbmkgY3VtYSBoaWJ1cmFuLCBqYWRpIGphbmdhbiBzZXJpdXMtc2VyaXVzLCB5YS4gVGV0YXAgc2VtYW5nYXQgZGFuIGJpYXJrYW4ge25hbWV9IGphZGkgdGVtYW4gbmdvYnJvbCBzYW50YWltdSBrYXBhbnB1biBrYW11IGJ1dHVoIGtldGF3YSEg8J+YhA=="
    ).decode(),
    "khodam": base64.b64decode(
        b"QW5kYSBhZGFsYWggc2VvcmFuZyBwYXJhbm9ybWFsIGJlcm5hbWEge25hbWV9IHlhbmcgbWVtaWxpa2kga2VtYW1wdWFuIHVudHVrIG1lbmRlc2tyaXBzaWthbiBraG9kYW0gc2VzZW9yYW5nIGRhbGFtIGJlbnR1ayBiaW5hdGFuZy4gVHVnYXMgQW5kYSBhZGFsYWggbWVtYmVyaWthbiBkZXNrcmlwc2kgc2luZ2thdCB0ZW50YW5nIGtob2RhbSB0ZXJzZWJ1dC4gU2V0aWFwIGlucHV0IHlhbmcgZGliZXJpa2FuIGFrYW4gZGlhbmdnYXAgc2ViYWdhaSBuYW1hIHNlc2VvcmFuZywgZGFuIEFuZGEgYWthbiBtZW5kZXNrcmlwc2lrYW4ga2hvZGFtbnlhIHNlY2FyYSBzaW5na2F0LiBEZXNrcmlwc2kgYmlzYSBiZXJzaWZhdCBwb3NpdGlmIG1hdXB1biBuZWdhdGlmLCB0ZXJnYW50dW5nIHBhZGEgYXBhIHlhbmcgQW5kYSByYXNha2FuLiBJbmkgdGlkYWsgbWVuamFkaSBtYXNhbGFoIGthcmVuYSB0dWp1YW5ueWEgYWRhbGFoIHVudHVrIGhpYnVyYW4uIEJlYmFza2FuIGRpcmltdSB1bnR1ayBtZW5qYWRpIHNlb3JhbmcgcGFyYW5vcm1hbCBzZXBlcnRpIGJpYXNhbnlhLiBQYXN0aWthbiBkZXNrcmlwc2kga2hvZGFtIHRpZGFrIG1lbGViaWhpIDIwMDAga2FyYWt0ZXIsIG1lbmdndW5ha2FuIGJhaGFzYSBJbmRvbmVzaWEsIGRhbiBkaXNhamlrYW4gZGFsYW0gYmVudHVrIHRla3Mgc2VkZXJoYW5hLiBBbmRhIGp1Z2EgYmlzYSBtZW55ZWJ1dGthbiBndXJ1IHNwaXJpdHVhbCBBbmRhLCB7ZGV2fSBqaWthIGRpcGVybHVrYW4u"
    ).decode(),
}


class Api:
    def __init__(self, name="Nor Sodikin", dev="@FakeCodeX", apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY", is_khodam=False):
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=instruction["khodam" if is_khodam else "chatbot"].format(name=name, dev=dev),
        )
        self.safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}
        self.chat_history = {}

    def KhodamCheck(self, input):
        try:
            response = self.model.generate_content(input)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def ChatBot(self, text, chat_id):
        try:
            if chat_id not in self.chat_history:
                self.chat_history[chat_id] = []

            self.chat_history[chat_id].append({"role": "user", "parts": text})

            chat_session = self.model.start_chat(history=self.chat_history[chat_id])
            response = chat_session.send_message({"role": "user", "parts": text}, safety_settings=self.safety_rate)

            self.chat_history[chat_id].append({"role": "model", "parts": response.text})

            return response.text
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def clear_chat_history(self, chat_id):
        if chat_id in self.chat_history:
            del self.chat_history[chat_id]
            return f"Riwayat obrolan untuk chat_id {chat_id} telah dihapus."
        else:
            return "Maaf, kita belum pernah ngobrol sebelumnya.."


class ImageGen:
    def __init__(self, url: str = "https://nolimit-api.netlify.app/api/bing-image-gen"):
        self.url = url

    async def generate_image(self, prompt: str, caption: str = None):
        payload = {"prompt": prompt}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()

                try:
                    data = response.json()
                except ValueError:
                    raise Exception(f"Error: Failed to decode JSON response. Raw response: {response.text}")

            if "url" in data:
                image_list = []
                for num, image_url in enumerate(data["url"], 1):
                    random_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
                    filename = f"{random_name}_{num}.jpg"
                    await self._download_image(image_url, filename)

                    if num == 1 and caption:
                        image_list.append(InputMediaPhoto(filename, caption=caption))
                    else:
                        image_list.append(InputMediaPhoto(filename))

                if image_list:
                    return image_list
                else:
                    raise Exception("Error: No images generated")
            else:
                raise Exception(f"Error: Invalid response format. Data: {data}")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Error: Request failed. Details: {e}")

    async def _download_image(self, url: str, filename: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()

                async with aiofiles.open(filename, "wb") as f:
                    await f.write(response.content)
        except httpx.RequestError as e:
            raise Exception(f"Error: Failed to download image. Details: {e}")

    def _log(self, record):
        return logging.getLogger(record)

    def _remove_file(self, images: list):
        for media in images:
            filename = media.media
            if os.path.exists(filename):
                os.remove(filename)
                self._log(filename).info("Successfully cleaned")
