import { NextResponse } from "next/server";
import { google } from "googleapis";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

async function getAuthClient() {
  const { data: tokenData } = await supabase
    .from("google_tokens")
    .select("*")
    .eq("id", "admin")
    .single();

  if (!tokenData) {
    throw new Error("Google Calendar bağlantısı yok");
  }

  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    `${process.env.NEXTAUTH_URL}/api/auth/google/callback`
  );

  oauth2Client.setCredentials({
    access_token: tokenData.access_token,
    refresh_token: tokenData.refresh_token,
    expiry_date: tokenData.expiry_date,
  });

  // Refresh token if expired
  oauth2Client.on("tokens", async (tokens) => {
    if (tokens.access_token) {
      await supabase
        .from("google_tokens")
        .update({
          access_token: tokens.access_token,
          expiry_date: tokens.expiry_date,
        })
        .eq("id", "admin");
    }
  });

  return oauth2Client;
}

// CREATE EVENT
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { date, time, duration, clientName, clientEmail } = body;

    const auth = await getAuthClient();
    const calendar = google.calendar({ version: "v3", auth });

    const startDateTime = `${date}T${time}:00+03:00`;
    const endDate = new Date(`${date}T${time}:00+03:00`);
    endDate.setMinutes(endDate.getMinutes() + (duration || 60));
    const endDateTime = endDate.toISOString();

    const event = {
      summary: `NextERA Seans - ${clientName}`,
      description: `Online danışmanlık seansı\nDanışan: ${clientName}\nE-posta: ${clientEmail}`,
      start: {
        dateTime: startDateTime,
        timeZone: "Europe/Istanbul",
      },
      end: {
        dateTime: endDateTime,
        timeZone: "Europe/Istanbul",
      },
      reminders: {
        useDefault: false,
        overrides: [
          { method: "email", minutes: 60 },
          { method: "popup", minutes: 30 },
        ],
      },
      attendees: clientEmail
        ? [{ email: clientEmail }]
        : [],
      conferenceData: {
        createRequest: {
          requestId: `nextera-${Date.now()}`,
          conferenceSolutionKey: { type: "hangoutsMeet" },
        },
      },
    };

    const response = await calendar.events.insert({
      calendarId: "primary",
      requestBody: event,
      conferenceDataVersion: 1,
      sendUpdates: "all",
    });

    return NextResponse.json({
      success: true,
      eventId: response.data.id,
      htmlLink: response.data.htmlLink,
      meetLink: response.data.conferenceData?.entryPoints?.[0]?.uri,
    });
  } catch (error: any) {
    console.error("Calendar event error:", error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}

// GET EVENTS
export async function GET(request: Request) {
  try {
    const auth = await getAuthClient();
    const calendar = google.calendar({ version: "v3", auth });

    const now = new Date();
    const response = await calendar.events.list({
      calendarId: "primary",
      timeMin: now.toISOString(),
      maxResults: 20,
      singleEvents: true,
      orderBy: "startTime",
      q: "NextERA",
    });

    return NextResponse.json({
      success: true,
      events: response.data.items,
    });
  } catch (error: any) {
    console.error("Calendar list error:", error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
