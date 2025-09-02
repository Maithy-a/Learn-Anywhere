# Learn-Anywhere PWA

Offline-first learning app built with **Next.js 15**, aligned with **SDG 4 (Quality Education)**.

[Live Demo](https://learn-anywhere.vercel.app/)


### 🚀 Quick Setup

```bash
# Clone repo
git clone https://github.com/Maithy-a/v0-learn-anywhere.git
cd v0-learn-anywhere-pwa

# Install dependencies
npm install

# Setup database
npm run db:setup

# Start dev server
npm run dev
```

Visit → [http://localhost:3000](http://localhost:3000)


### 🔑 Env Vars (`.env.local`)

```env
JWT_SECRET=your-secret-key
PAYSTACK_SECRET_KEY=sk_test_your_key
NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY=pk_test_your_key
XAI_API_KEY=your-xai-api-key
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 🛠️ Tech Stack

* Next.js 15 (App Router)
* Tailwind + Shadcn/ui
* SQLite + JWT Auth
* Paystack (payments)
* Grok AI (quiz generation)
* PWA (offline support)


### 📄 License

MIT - free to use & modify.
<br>

⚡ That’s it! Clone → Install → Run.
