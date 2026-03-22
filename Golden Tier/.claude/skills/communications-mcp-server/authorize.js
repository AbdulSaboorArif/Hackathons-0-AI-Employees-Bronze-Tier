#!/usr/bin/env node

/**
 * Gmail OAuth2 Authorization Script
 * Generates token.json for Gmail API access
 */

import { google } from 'googleapis';
import fs from 'fs/promises';
import http from 'http';
import { URL } from 'url';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];
const TOKEN_PATH = path.join(__dirname, '../../../token.json');
const CREDENTIALS_PATH = path.join(__dirname, '../../../credential.json');

async function authorize() {
  try {
    // Load credentials
    const credentialsContent = await fs.readFile(CREDENTIALS_PATH, 'utf-8');
    const credentials = JSON.parse(credentialsContent);

    const { client_secret, client_id, redirect_uris } = credentials.installed;

    // Use localhost redirect
    const redirectUri = 'http://localhost:3000/oauth2callback';

    const oAuth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirectUri
    );

    // Generate authorization URL
    const authUrl = oAuth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: SCOPES,
    });

    console.log('\n' + '='.repeat(60));
    console.log('Gmail OAuth2 Authorization');
    console.log('='.repeat(60));
    console.log('\n[*] Please open this URL in your browser:\n');
    console.log(authUrl);
    console.log('\n[*] Waiting for authorization...');
    console.log('[*] Local server listening on http://localhost:3000\n');

    // Create temporary HTTP server to receive callback
    const server = http.createServer(async (req, res) => {
      try {
        const url = new URL(req.url, `http://localhost:3000`);

        if (url.pathname === '/oauth2callback') {
          const code = url.searchParams.get('code');

          if (code) {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(`
              <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                  <h1 style="color: green;">Authorization Successful!</h1>
                  <p>You can close this window and return to the terminal.</p>
                </body>
              </html>
            `);

            // Exchange code for token
            const { tokens } = await oAuth2Client.getToken(code);

            // Save token
            await fs.writeFile(TOKEN_PATH, JSON.stringify(tokens, null, 2));

            console.log('\n[OK] Authorization successful!');
            console.log(`[OK] Token saved to: ${TOKEN_PATH}`);
            console.log('\n' + '='.repeat(60));
            console.log('Gmail API is now ready to use');
            console.log('='.repeat(60) + '\n');

            server.close();
            process.exit(0);
          } else {
            res.writeHead(400, { 'Content-Type': 'text/plain' });
            res.end('Error: No authorization code received');
            server.close();
            process.exit(1);
          }
        }
      } catch (error) {
        console.error('[ERROR]', error.message);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error: ' + error.message);
        server.close();
        process.exit(1);
      }
    });

    server.listen(3000, () => {
      console.log('[INFO] Server started successfully');
    });

    // Timeout after 5 minutes
    setTimeout(() => {
      console.log('\n[ERROR] Authorization timeout (5 minutes)');
      server.close();
      process.exit(1);
    }, 300000);

  } catch (error) {
    console.error('\n[ERROR] Authorization failed:', error.message);

    if (error.code === 'ENOENT') {
      console.error(`\n[ERROR] File not found: ${error.path}`);
      console.error('[INFO] Make sure credential.json exists in the project root');
    }

    process.exit(1);
  }
}

// Run authorization
authorize();
