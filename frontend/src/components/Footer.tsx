import { SiGithub, SiX } from 'react-icons/si';
import { FaLinkedin } from 'react-icons/fa6';

const socialLinks = [
  { href: 'https://github.com', icon: <SiGithub className="w-5 h-5" />, label: 'GitHub' },
  { href: 'https://x.com', icon: <SiX className="w-5 h-5" />, label: 'X (Twitter)' },
  { href: 'https://linkedin.com', icon: <FaLinkedin className="w-5 h-5" />, label: 'LinkedIn' },
];

const quickLinks = [
  { href: '#', label: 'About' },
  { href: '#', label: 'Privacy' },
  { href: '#', label: 'Terms' },
];

export default function Footer() {
  return (
    <footer className="relative border-t border-border mt-24">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="text-center md:text-left">
            <h3 className="text-lg font-bold text-foreground">
              Scene<span className="text-primary">Scribe</span>
            </h3>
            <p className="text-sm text-foreground/50 mt-1">
              AI-powered video captioning, reimagined.
            </p>
          </div>

          <nav className="flex items-center gap-6" aria-label="Footer navigation">
            {quickLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-sm text-foreground/50 hover:text-foreground transition-colors duration-200 cursor-pointer focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
              >
                {link.label}
              </a>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={social.label}
                className="w-10 h-10 rounded-xl bg-surface flex items-center justify-center text-foreground/50 hover:text-foreground hover:bg-white/10 transition-all duration-200 cursor-pointer focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
              >
                {social.icon}
              </a>
            ))}
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-foreground/40">
            &copy; {new Date().getFullYear()} SceneScribe. All rights reserved.
          </p>
          <span className="text-xs font-medium text-foreground/40 px-3 py-1.5 rounded-full bg-surface">
            Built for AMD Hackathon Act II
          </span>
        </div>
      </div>
    </footer>
  );
}