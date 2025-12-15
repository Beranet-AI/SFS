// app/api/alerts/route.ts
export async function GET() {
  const res = await fetch(
    `${process.env.MANAGEMENT_API}/api/v1/alerts/active/`,
    { cache: 'no-store' },
  )
  return Response.json(await res.json())
}
