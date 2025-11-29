// src/app/api/readings/route.ts
import { NextResponse } from "next/server";

const DJANGO_API_BASE_URL = process.env.DJANGO_API_BASE_URL;
const DJANGO_API_TOKEN = process.env.DJANGO_API_TOKEN;

export async function GET() {
  if (!DJANGO_API_BASE_URL || !DJANGO_API_TOKEN) {
    return NextResponse.json(
      { detail: "DJANGO_API_BASE_URL یا DJANGO_API_TOKEN تنظیم نشده است." },
      { status: 500 }
    );
  }

  try {
    // آدرس جنگو – اینجا فرض می‌کنیم env این شکلی ست شده:
    // DJANGO_API_BASE_URL=http://127.0.0.1:8000/api/v1
    const url = `${DJANGO_API_BASE_URL}/sensor-readings/`;

    const resp = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${DJANGO_API_TOKEN}`,
        Accept: "application/json",
      },
    });

    if (!resp.ok) {
      const text = await resp.text();
      return NextResponse.json(
        {
          detail: "Error fetching readings from Django",
          status: resp.status,
          body: text,
        },
        { status: 500 }
      );
    }

    const data = await resp.json();

    // اگر DRF pagination روشن باشد، data.results آرایه است
    const readings = Array.isArray(data) ? data : (data as any).results ?? data;

    return NextResponse.json({ readings });
  } catch (err: any) {
    return NextResponse.json(
      { detail: "Exception while calling Django", error: String(err) },
      { status: 500 }
    );
  }
}
