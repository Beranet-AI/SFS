import { NextRequest, NextResponse } from "next/server";

const resolveBase = () =>
  process.env.DJANGO_API_BASE_URL || process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL;

const resolveToken = () =>
  process.env.DJANGO_API_TOKEN || process.env.NEXT_PUBLIC_DJANGO_API_TOKEN || process.env.NEXT_PUBLIC_FASTAPI_TOKEN;

const ensureTrailingSlash = (base: string) => (base.endsWith("/") ? base : `${base}/`);

export async function GET(request: NextRequest) {
  const base = resolveBase();
  const token = resolveToken();

  if (!base || !token) {
    return NextResponse.json(
      { detail: "DJANGO_API_BASE_URL یا DJANGO_API_TOKEN تنظیم نشده است." },
      { status: 500 }
    );
  }

  try {
    const searchParams = request.nextUrl.searchParams;
    const sensorId = searchParams.get("sensor_id");
    const limit = searchParams.get("limit") || "20";

    const url = new URL("alerts/active/", ensureTrailingSlash(base));
    if (sensorId) {
      url.searchParams.set("sensor_id", sensorId);
    }
    url.searchParams.set("limit", limit);

    const resp = await fetch(url.toString(), {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
        Accept: "application/json",
      },
    });

    if (!resp.ok) {
      const text = await resp.text();
      return NextResponse.json(
        { detail: "Error fetching alerts", status: resp.status, body: text },
        { status: 500 }
      );
    }

    const data = await resp.json();
    const alerts = (data as any).alerts ?? [];

    return NextResponse.json({ alerts });
  } catch (err: any) {
    return NextResponse.json(
      { detail: "Exception while calling Django", error: String(err) },
      { status: 500 }
    );
  }
}
