
"use client"; // Add this line to declare the component as a client component

import { useState, ChangeEvent, FormEvent } from "react";
import Link from "next/link";
export default function Home() {


  return (
    <div className="flex flex-col sm:flex-row gap-8 items-center justify-center mt-8">

    <Link href="/OurInsights">
      <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
        Carbon Emission Model
      </button>
    </Link>
    <Link href="/methaneemission">
      <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
        Methane Emission Model
      </button>
    </Link>
    <Link href="/Factors">
      <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
        Factors Affecting GHG Emission
      </button>
    </Link>
    <Link href="/GetYourOwnInsights">
      <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
        Effects of cimate change
      </button>
    </Link>
  </div>
    );
}
 