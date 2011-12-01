#/usr/bin/env ruby
def hamming(length)
  hammingsequence = [1]
  count = 0 
  begin
    newhamming = [2*hammingsequence[count],3*hammingsequence[count],5*hammingsequence[count]]
    newhamming.each do 
     |n| puts "#{n}" 
    end
    puts "----"
    newhamming.each do |n|
      if not hammingsequence.include?(n)
        hammingsequence.push(n)
      end
    end
    count = count + 1
    hammingsequence.sort!
  end while hammingsequence.size < length
  hammingsequence = hammingsequence[0,length]
  hammingsequence.each do
   |n| print "#{n} "
  end
end

hamming(20)
puts ""
