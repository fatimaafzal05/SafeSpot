"use client";
import dynamic from "next/dynamic";
const CommunityMap = dynamic(() => import("./CommunityMap").then(module => module.CommunityMap), { ssr: false, loading: () => <div className="card empty">Loading the community map…</div> });
export default CommunityMap;
