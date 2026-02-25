import { NextResponse } from "next/server";
import { google } from "googleapis";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");

  if (!code) {
    return NextResponse.redirect(
      `${process.env.NEXTAUTH_URL}?error=no_code`
    );
  }

  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    `${process.env.NEXTAUTH_URL}/api/auth/google/callback`
  );

  try {
    const { tokens } = await oauth2Client.getToken(code);

    // Store tokens in Supabase
    // We'll store in a google_tokens table
    if (tokens.refresh_token) {
      await supabase.from("google_tokens").upsert({
        id: "admin",
        access_token: tokens.access_token,
        refresh_token: tokens.refresh_token,
        expiry_date: tokens.expiry_date,
      });
    }

    return NextResponse.redirect(
      `${process.env.NEXTAUTH_URL}?google=connected`
    );
  } catch (error) {
    console.error("Google auth error:", error);
    return NextResponse.redirect(
      `${process.env.NEXTAUTH_URL}?error=auth_failed`
    );
  }
}
