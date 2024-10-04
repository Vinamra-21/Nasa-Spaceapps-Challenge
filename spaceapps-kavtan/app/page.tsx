import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-gray-900 text-white">
      <header className="row-start-1">
        <h1 className="text-6xl sm:text-8xl font-extrabold tracking-wide text-center">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
            GHG
          </span>
          <span className=""> by Team Kavtan</span>
        </h1>
      </header>

      <main className="row-start-2 flex flex-col sm:flex-row gap-8 items-center justify-center">
        <Link href="/OurInsights">
          <button className="text-white font-bold py-4 px-10 rounded-lg text-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 shadow-lg transition-transform transform hover:scale-105">
            Our Insights
          </button>
        </Link>
        
        <Link href="/GetYourOwnInsights">
          <button className="text-white font-bold py-4 px-10 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
            Your Insights
          </button>
        </Link>
      </main>

      {/* Footer */}
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <span>Team Kavtan</span>
        <Image
          aria-hidden
          src="https://nextjs.org/icons/globe.svg"
          alt="Globe icon"
          width={16}
          height={16}
        />
      </footer>
    </div>
  );
}
