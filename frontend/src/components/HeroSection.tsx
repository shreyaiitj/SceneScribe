import { motion } from 'framer-motion';
import { HiOutlineArrowDown } from 'react-icons/hi2';

function FloatingShape({
  className,
  delay = 0,
  size = 60,
}: {
  className: string;
  delay?: number;
  size?: number;
}) {
  return (
    <motion.div
      className={`absolute rounded-full opacity-20 ${className}`}
      style={{ width: size, height: size }}
      animate={{
        y: [0, -30, 0],
        x: [0, 15, 0],
        rotate: [0, 10, 0],
      }}
      transition={{
        duration: 6 + delay,
        repeat: Infinity,
        ease: 'easeInOut',
        delay,
      }}
    />
  );
}

export default function HeroSection() {
  const scrollToUpload = () => {
    const el = document.getElementById('upload');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden px-4">
      <div
        className="absolute inset-0 animate-gradient"
        style={{
          background:
            'radial-gradient(ellipse 80% 60% at 50% 0%, rgba(124,58,237,0.15) 0%, transparent 60%), ' +
            'radial-gradient(ellipse 60% 50% at 80% 80%, rgba(6,182,212,0.1) 0%, transparent 50%), ' +
            'radial-gradient(ellipse 50% 40% at 20% 70%, rgba(124,58,237,0.08) 0%, transparent 50%)',
        }}
      />

      <FloatingShape
        className="bg-primary top-20 left-[10%]"
        delay={0}
        size={80}
      />
      <FloatingShape
        className="bg-secondary top-40 right-[15%]"
        delay={1.5}
        size={50}
      />
      <FloatingShape
        className="bg-purple bottom-40 left-[20%]"
        delay={3}
        size={60}
      />
      <FloatingShape
        className="bg-cyan bottom-60 right-[25%]"
        delay={2}
        size={40}
      />

      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />

      <div className="relative z-10 text-center max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold mb-8"
        >
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
          AI-Powered Captioning
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-foreground leading-tight"
        >
          Captions that{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
            speak volumes
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-lg md:text-xl text-foreground/60 mt-6 max-w-2xl mx-auto leading-relaxed"
        >
          Upload any video or paste a URL. SceneScribe uses AI to generate captions
          in 4 unique styles — Formal, Sarcastic, and two flavors of Humor — with
          confidence scoring.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10"
        >
          <button
            onClick={scrollToUpload}
            className="group inline-flex items-center gap-2.5 px-8 py-4 rounded-2xl bg-primary text-on-primary font-semibold text-base
              transition-all duration-200 ease-out cursor-pointer
              hover:opacity-90 hover:scale-[1.02]
              active:scale-[0.97]
              focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2
              shadow-lg shadow-primary/25"
            aria-label="Get started — scroll to upload section"
          >
            Get Started
            <HiOutlineArrowDown className="w-5 h-5 group-hover:translate-y-0.5 transition-transform duration-200" />
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-16 flex flex-wrap items-center justify-center gap-8 text-foreground/30 text-xs font-medium"
        >
          <span className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            AMD-Powered
          </span>
          <span className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            4 Caption Styles
          </span>
          <span className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            Confidence Scoring
          </span>
          <span className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/></svg>
            AMD Hackathon Act II
          </span>
        </motion.div>
      </div>

      <motion.button
        onClick={scrollToUpload}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1, y: [0, 8, 0] }}
        transition={{ duration: 2, repeat: Infinity, delay: 1.5 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 text-foreground/30 hover:text-foreground/60 transition-colors duration-200 cursor-pointer focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
        aria-label="Scroll down to upload section"
      >
        <HiOutlineArrowDown className="w-6 h-6" />
      </motion.button>
    </section>
  );
}