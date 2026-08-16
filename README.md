# Shmry Software Inc

**One ecosystem. Seven specialized systems.**

Shmry is the cloud, email, compute, storage, Git and artifact infrastructure layer for the Shmry Software Inc ecosystem. It is designed to work independently and to provide additional capabilities to peer software when they need cloud or service functionality.

## Products

| Software | Role |
|---|---|
| **Shmry** | Cloud + email server, compute, storage, Git and artifacts |
| **Xerus** | Disk-first persistent memory and retrieval |
| **VPS** | Native C++ TLS/SNI webserver and reverse proxy |
| **HuobzLang** | Highest-level compact language and semantic representation |
| **Neuron** | Experimental biological intelligence engine |
| **Nifdu** | Native screenshot/browser verification and repair harness |
| **Sophyane** | Local-first multi-option software-engineering harness |

All components share the `sophyane-ecosystem-v1` capability contract. A component may request a peer capability when that capability is unavailable locally.

## Download everything

Linux, macOS, WSL, ChromeOS Linux and Termux:

```bash
curl -fsSL https://raw.githubusercontent.com/badrpk/shmry/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/badrpk/shmry/main/install.ps1 | iex
```

Install one product by passing its name:

```bash
curl -fsSL https://raw.githubusercontent.com/badrpk/shmry/main/install.sh -o /tmp/shmry-install.sh
bash /tmp/shmry-install.sh sophyane
```

The universal downloader is conservative: it invokes native product installers only where an installer is currently available and otherwise installs the source repository without claiming unsupported platform verification.

## Website

The public website is designed for Vercel static deployment.

- `/` — main Shmry site
- `/downloads` — ecosystem download center
- `/products` — product catalog
- `/architecture` — architecture information
- `/status` — status page

Public Vercel configuration no longer embeds private or machine-specific backend addresses. Runtime service endpoints should be supplied through deployment configuration rather than committed into the repository.

## Architecture

```text
Applications / Users
        |
        v
Sophyane -------- Nifdu
   |                |
   |                +--> visual/browser verification
   |
   +--> Xerus ------+--> disk-first memory
   +--> Neuron --------> biological intelligence
   +--> HuobzLang -----> compact semantic language
   +--> Shmry ----------> cloud / email / compute / storage / Git
   +--> VPS ------------> TLS / HTTPS network boundary
```

Every software package remains independently usable. Ecosystem routing is an additional capability layer rather than a hard dependency on every peer.

## Security

Never commit:

- passwords or application passwords
- API tokens
- private TLS keys
- ACME account state
- `.env` files containing secrets
- machine-specific credentials
- private runtime databases or logs

Use environment variables and deployment secret stores for runtime credentials.

## Development

```bash
git clone https://github.com/badrpk/shmry.git
cd shmry
npm install
```

The repository contains the public website, product pages, service prototypes, deployment tooling and ecosystem manifests. Some older modules remain transitional and should not be interpreted as production-verified across every operating system.

## Ecosystem repositories

- `badrpk/shmry`
- `badrpk/xerus`
- `badrpk/vps`
- `badrpk/HuobzLang`
- `badrpk/neuron`
- `badrpk/nifdu`
- `badrpk/sophyane`

## Contributing

Issues and pull requests are welcome. Keep product boundaries clear, avoid committing generated dependency trees, and document any new cross-product capability in the shared ecosystem contract.
