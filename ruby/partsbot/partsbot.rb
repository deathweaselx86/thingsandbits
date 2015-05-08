#!/usr/bin/env ruby

require 'byebug'
require 'cinch'
require 'json'
require 'net/http'


BASE_OCTOPART_URL = "https://octopart.com/api/v3/parts/match?".freeze
OCTOPART_API_KEY_SUFFIX = "&apikey=#{ENV['OCTOPART_API_KEY']}".freeze

bot = Cinch::Bot.new do
  configure do |c|
    c.server = "irc.freenode.org"
    c.channels = ["#testjessroom"]
    c.nick = "partsbot"
    c.user = "nothingtoseehere"
  end

  on :message, /lookup datasheet ([\w|\-]+)/ do |m, mpn|
    m.reply "Looking up Octopart information for #{mpn}"
    response = get_mpn_info(mpn)
    m.reply "Found the following datasheets."
    response.each do |result|
      m.reply "<#{mpn} datasheet> #{result}"
    end
  end
end

def get_mpn_info(mpn)
  query = {limit: 1, 
           mpn_or_sku: mpn}
  url = BASE_OCTOPART_URL +
        '&queries=' + URI.encode(JSON.generate([query])) +
        '&include[]=datasheets' +
        OCTOPART_API_KEY_SUFFIX
  response = JSON.parse(Net::HTTP.get_response(URI.parse(url)).body)
  begin
    datasheets = response["results"][0]["items"][0]["datasheets"].collect do |x|
      x["url"]
    end
    datasheets.take 5
  rescue
    ["No datasheets found"]
  end
end

bot.start
