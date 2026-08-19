export const categories = ["Unsafe Street", "Poor Lighting", "Traffic Danger", "Harassment Concern", "Suspicious Activity", "Other"] as const;
export type Category = typeof categories[number];
export type Status = "pending" | "approved" | "rejected" | "hidden";
export interface Report { id:number; category:Category; title:string; description:string; latitude:number|null; longitude:number|null; approximate_location_name:string; incident_at:string|null; created_at:string; status:Status; upvote_count:number; }
export interface Analytics { total:number; reports_this_week:number; category_counts:Record<Category,number>; trend:{date:string;count:number}[]; recent:Report[]; }
