# Ai vtuber/assistance
This project is an AI VTuber and virtual assistant framework designed to serve as a foundation for building your own AI-powered VTuber or intelligent assistant. Whether you're a developer looking to launch an AI-driven VTuber startup or simply exploring AI-enhanced virtual personalities, this codebase provides a solid starting point.

Built on top of the Agno agentic framework (python 3.10 prefered), the project supports advanced features such as session management, memory, function calling, and more—making it easy to implement complex AI behaviors and interactivity.

A complete frontend UI with live 2d model is also included, fully integrated with the Agno backend API to provide a seamless development and user experience. The codebase is cleanly structured and modular, with extensibility in mind, allowing developers to easily add new features or improve existing ones. This project is designed to run locally in your browser via localhost.

Note: This project is not under active development or maintenance.

![Demo](/storage/demo/aivt_demo.gif)

## Features
### Backend (fastapi)
- [x] Session and memory for agent (saved as sqlite in local dir)
- [x] Tooling for agent such as search engine
- [x] Use agent on terminal (py script)
- [x] use agent on api
- [x] Use agent on discord as assistant
- [ ] Text to speech + voice clone
### Frontend (vue)
- [x] Load your live2d model (can interact depend on model created)
- [x] Capture screen display
- [x] Chat using chat-ui
- [ ] Chat using mic
- [ ] Response by voice and lipsync

## Getting started
```sh
// on linux os
git clone this_repo
cd this_repo
cp .env.example .env
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ui
pnpm install

// if during develpoment
pnpm dev
cd ..
python main.py (access ui from port: 5173, api from port: 7777)

// if during production
pnpm build
cd ..
python main.py (access everything from port: 7777)
```

## Project layout
```sh
project/
├── core/
│   ├── agents/ (ai agent)
│   │   ├── base_agent.py
│   │   └── mao.py
│   ├── facades/ (custom service)
│   │   └── discord_client.py
│   ├── tools/ (custom toolkit)
│   └── configs.py (env configs loaded in python)
├── storage/
│   └── db/ (sqlite database)
│       └── Mao.db
├── ui/
│   ├── dist/ (builded frontend)
│   ├── public/
│   ├── src/ (vue codebase)
│   ├── index.html
│   └── vite.config.js
├── .env
├── main.py (python fastapi server)
└── requirements.txt
```

## Reference and external source
- [Agno](https://docs.agno.com/introduction)
- [Fastapi](https://fastapi.tiangolo.com/)
- [Pixi js](https://pixijs.com/)
- [pixi-live2d-display-lipsyncpatch](https://www.npmjs.com/package/pixi-live2d-display-lipsyncpatch)
- [Live2D Cubism4 SDK](https://www.live2d.com/en/sdk/download/web/)
- [Mao live2D model](https://www.live2d.com/en/learn/sample/)
- [Tamamo live2D model](https://poblanc.booth.pm/)