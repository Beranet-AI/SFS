// src/app/api/management/incidents/route.ts
import { NextResponse } from "next/server";

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API;

export async function GET(req: Request) {
  if (!BASE) {
    return NextResponse.json(
      { error: "NEXT_PUBLIC_MANAGEMENT_API is not set" },
      { status: 500 }
    );
  }

  // Backend هنوز event می‌گوید (طبق تصمیم: backend دست نخورَد)
  const upstream = `${BASE}/api/v1/events/`;

  const res = await fetch(upstream, {
    method: "GET",
    headers: {
      // cookie/session را عبور می‌دهیم تا auth خراب نشود
      cookie: req.headers.get("cookie") ?? "",
      accept: "application/json",
    },
    cache: "no-store",
  });

  const contentType = res.headers.get("content-type") ?? "";

  // اگر JSON بود همون رو پاس بده، اگر نبود متن رو بده (برای دیباگ 404 های backend)
  if (contentType.includes("application/json")) {
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } else {
    const text = await res.text();
    return new NextResponse(text, {
      status: res.status,
      headers: { "content-type": contentType || "text/plain" },
    });
  }
}
