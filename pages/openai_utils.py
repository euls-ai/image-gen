from openai import OpenAI
import requests
import streamlit as st

client = OpenAI(api_key=st.secrets.o_ck)


def get_total_cost() -> float:
    total_cost = 0.0

    resp = requests.get(
        st.secrets.o_cu,
        params={
            "start_time": "1748770209",
            "project_ids": [st.secrets.p_id],
            "limit": 180,
        },
        headers={"Authorization": f"Bearer {st.secrets.o_ak}"},
    )
    resp = resp.json()
    for i in resp["data"]:
        if i["results"]:
            for j in i["results"]:
                total_cost += j["amount"]["value"]
    return total_cost


def just_img(prompt: str, user_text: str, img_url: str) -> str:
    response = client.responses.create(
        model=st.secrets.o_mc,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": st.secrets[prompt]}],
            },
            {"role": "user", "content": [{"type": "input_text", "text": user_text}]},
            {
                "role": "user",
                "content": [{"type": "input_image", "image_url": img_url}],
            },
        ],
        tools=[
            {
                "type": "image_generation",
                "quality": "high",
                "model": "gpt-image-1",
            }
        ],
        store=False,
    )

    model_img = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    return model_img.pop() if model_img else None
