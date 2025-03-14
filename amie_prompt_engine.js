// src/amie_prompt_engine.js
// Function to generate a dynamic prompt with context injection and chaining.
export function buildDynamicPrompt(context, userInput) {
  const basePrompt = `You are Amie, a compassionate SEL assistant.
A user says: "${userInput}".
User context: ${JSON.stringify(context)}.
Provide supportive, empathetic, and actionable advice.`;
  return basePrompt;
}

// Example usage:
const userContext = { mood: "anxious", previousMessages: ["I have many deadlines."] };
const userInput = "I'm worried about my exam tomorrow.";
const prompt = buildDynamicPrompt(userContext, userInput);
console.log("Dynamic Prompt:", prompt);
