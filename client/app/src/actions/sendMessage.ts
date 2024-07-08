"use server";

import { AUTHOR_TYPES } from "../types";

export async function sendMessage(query: string) {
  const response = await fetch("http://46.101.204.250/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });
  const responseData = await response.json();

  return { author: AUTHOR_TYPES.BOT, body: responseData["chat_gpt_answer"] };
}