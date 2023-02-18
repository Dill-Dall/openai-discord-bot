<div class="markdown prose w-full break-words dark:prose-invert dark">
	<h1>OpenAI Discord Bot
	</h1>
	<p>The <code>openai-discord-bot</code> project is a Python-based Discord bot that uses OpenAI's API to generate
		natural language responses and images in response to user commands.</p>
	<h2>Getting started</h2>
	<p>To use the <code>openai-discord-bot</code> project, you will need to:</p>
	<ol>
		<li>Clone the repository to your local machine.</li>
		<li>Install the required Python packages using <code>pip install -r requirements.txt</code>.</li>
		<li>Set up the necessary environment variables in a <code>.env</code> file in the root directory of the project.
			The required environment variables are:</li>
	</ol>
	<ul>
		<li><code>DISCORD_TOKEN</code>: Your Discord bot token. -> <a href="https://discordapp.com/developers/applications">discord developer</a></li>
		<li><code>OPENAI_API_KEY</code>: Your OpenAI API key.  -> <a href="https://openai.com/api/">openai.com/api</a></li> 
	</ul>
	<ol start="4">
		<li>Start the bot by running <code>python discord_bot.py</code>.</li>
	</ol>
	<h2>Docker usage</h2>
		<p>To run the app on a server:</p>
	<pre><div class="bg-black mb-4 rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans"><span class="">bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">
	1 - Install Docker
	2 - $ cp .env.example .env
	3 - Then input the require values into the .env keys
	4 - docker run --env-file .env --rm --name discord-openai-bot thomda/openai-discord-bot:latest
</code></div></div></pre>
	<h2>Usage</h2>
	<p>The <code>openai-discord-bot</code> project provides several slash commands that trigger different OpenAI models
		to generate responses to user queries:</p>
	<ul>
		<li><code>/glados</code>: Generates a quote or comment from the GLaDOS AI model.</li>
		<li><code>/timmy</code>: Generates a response to a user's question using the TIMMY AI model.</li>
		<li><code>/glen</code>: Generates a short and concise answer to a user's question using the GLEN AI model.</li>
		<li><code>/dall</code>: Generates an image from the DALL-E AI model using the specified prompt.</li>
	</ul>
	<p>To use the bot, simply type one of these commands in a Discord channel where the bot is present, followed by any
		additional required parameters.</p>
	<h2>Contributing</h2>
	<p>If you want to contribute to the <code>openai-discord-bot</code> project, feel free to fork the repository and
		submit a pull request with your changes. All kinds of contributions are welcome, including bug fixes, new
		features, and improvements to the existing code.</p>
	<h2>Refferences</h2>
	<ul>
	<li><a href="https://docs.pycord.dev">pycord</a></li>
	<li><a href="https://openai.com/api/">openai.com/api</a></li>
	</ul>
	
</div>