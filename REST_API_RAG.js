// src/index.js
const express = require('express');
const cors = require('cors');
const openai = require('openai');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

// Configure OpenAI API Key
openai.apiKey = process.env.OPENAI_API_KEY;

// Middleware
app.use(bodyParser.json());
app.use(cors({
  origin: ['https://cordz-del.github.io'],
  credentials: true
}));

// Example endpoint: Accepts a user query, retrieves context (mocked), and generates a response using GPT-4.
app.post('/api/query', async (req, res) => {
  try {
    const { query, userContext } = req.body;
    
    // Mock retrieval: In a real system, query your vector DB here.
    const retrievedContext = "Relevant context from vector database.";
    
    // Combine query and context into an optimized prompt.
    const prompt = `You are Amie, a compassionate SEL assistant. User context: ${JSON.stringify(userContext)}. 
User Query: "${query}". 
Additional Context: "${retrievedContext}". 
Provide supportive and actionable advice.`;
    
    // Generate GPT-4 response.
    const response = await openai.ChatCompletion.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are Amie, a compassionate SEL assistant." },
        { role: "user", content: prompt }
      ],
      max_tokens: 150,
      temperature: 0.7
    });
    
    res.json({
      response: response.choices[0].message.content.trim()
    });
  } catch (error) {
    console.error("Error in /api/query:", error);
    res.status(500).json({ error: "Failed to process the query." });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
