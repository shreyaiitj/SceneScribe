import { motion } from 'framer-motion';
import { HiOutlineCloudArrowUp, HiOutlineMagnifyingGlass, HiOutlineSparkles } from 'react-icons/hi2';

const steps = [
  {
    icon: <HiOutlineCloudArrowUp className="w-8 h-8" />,
    title: 'Upload',
    description: 'Drop a video file or paste a URL. We support MP4, MOV, AVI, and WEBM formats up to 100MB.',
    color: 'from-primary/40 to-primary/10',
    iconColor: 'text-primary',
  },
  {
    icon: <HiOutlineMagnifyingGlass className="w-8 h-8" />,
    title: 'Analyze',
    description: 'Our AI analyzes every scene, detecting objects, actions, and context across all frames.',
    color: 'from-secondary/40 to-secondary/10',
    iconColor: 'text-secondary',
  },
  {
    icon: <HiOutlineSparkles className="w-8 h-8" />,
    title: 'Generate',
    description: 'Get 4 unique caption styles with confidence scores — Formal, Sarcastic, Humorous Tech & Non-Tech.',
    color: 'from-purple/40 to-purple/10',
    iconColor: 'text-purple',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <span className="text-xs font-semibold tracking-widest uppercase text-primary">
            How It Works
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mt-3">
            Three steps to perfect captions
          </h2>
          <p className="text-foreground/60 mt-3 max-w-xl mx-auto">
            No complex setup — just upload, analyze, and get AI-generated captions in seconds.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.5, delay: i * 0.15, ease: 'easeOut' }}
              className="relative"
            >
              <div className="flex items-center justify-center w-12 h-12 rounded-full bg-muted text-foreground/50 text-sm font-bold mb-6">
                {i + 1}
              </div>

              <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center mb-5 ${step.iconColor}`}>
                {step.icon}
              </div>

              <h3 className="text-xl font-semibold text-foreground mb-3">
                {step.title}
              </h3>
              <p className="text-foreground/60 text-sm leading-relaxed">
                {step.description}
              </p>

              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-6 left-16 w-[calc(100%-4rem)] h-px bg-gradient-to-r from-border to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}