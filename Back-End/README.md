Back-End setup

This backend expects a GROQ API key in the environment variable `GROQ_API_KEY`.

Options to provide the key:

- Use a local `.env` file (recommended for development):
  1. Copy `.env.example` to `.env` in the `Back-End` folder.
  2. Put your key: `GROQ_API_KEY=your_groq_api_key_here`.

- Set for the current PowerShell session (temporary):

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
python app.py
```

- Persist the key on Windows (applies to new shells after restart):

```powershell
setx GROQ_API_KEY "your_groq_api_key_here"
# close and reopen PowerShell to pick up the new value
```

Troubleshooting:
- To check the current value in PowerShell:

```powershell
echo $env:GROQ_API_KEY
```

- If you see a runtime error that the key is missing, ensure you set the env var or created a `.env` file in the `Back-End` folder. The app uses `python-dotenv` to load `.env` automatically.
