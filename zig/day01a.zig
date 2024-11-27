const std = @import("std");

const INPUT = @embedFile("day01.txt");

fn solve(input: []const u8) usize {
    var res: usize = 0;
    var iter = std.mem.tokenizeAny(u8, input, "\n");
    while (iter.next()) |line| {
        var d1: u8 = 0;
        var d0: u8 = 0;
        for (line) |char| {
            if (std.ascii.isDigit(char)) {
                d0 = char - '0';
                if (d1 == 0) d1 = d0;
            }
        }
        res += 10 * d1 + d0;
    }
    return res;
}

pub fn main() !void {
    const solution = solve(INPUT);
    std.debug.print("{}\n", .{solution});
}

const SAMPLE =
    \\1abc2
    \\pqr3stu8vwx
    \\a1b2c3d4e5f
    \\treb7uchet
;

test "sample" {
    try std.testing.expectEqual(142, solve(SAMPLE));
}
