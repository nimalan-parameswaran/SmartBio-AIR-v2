import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  
  useEffect(() => {
    router.replace("/dashboard");
  }, [router]);
  
  return (
    <div className="min-h-screen bg-[#090d0b] flex items-center justify-center text-[#e2f0e7]">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium opacity-75">Redirecting to Smart BIO AIR Dashboard...</p>
      </div>
    </div>
  );
}
