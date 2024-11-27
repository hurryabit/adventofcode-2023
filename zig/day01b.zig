const std = @import("std");

const INPUT = @embedFile("day01.txt");

const DIGITS = [_]struct { name: []const u8, value: u8 }{
    .{ .name = "one", .value = 1 },
    .{ .name = "two", .value = 2 },
    .{ .name = "three", .value = 3 },
    .{ .name = "four", .value = 4 },
    .{ .name = "five", .value = 5 },
    .{ .name = "six", .value = 6 },
    .{ .name = "seven", .value = 7 },
    .{ .name = "eight", .value = 8 },
    .{ .name = "nine", .value = 9 },
};

fn solve(input: []const u8) usize {
    var res: usize = 0;
    var iter = std.mem.tokenizeAny(u8, input, "\n");
    while (iter.next()) |line| {
        var d1: u8 = 0;
        var d0: u8 = 0;
        for (line, 0..) |char, index| {
            var optD: ?u8 = null;
            if (std.ascii.isDigit(char)) {
                optD = char - '0';
            } else for (DIGITS) |digit| {
                if (std.mem.startsWith(u8, line[index..], digit.name)) {
                    optD = digit.value;
                    break;
                }
            }
            if (optD) |d| {
                if (d1 == 0) d1 = d;
                d0 = d;
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
    \\two1nine
    \\eightwothree
    \\abcone2threexyz
    \\xtwone3four
    \\4nineeightseven2
    \\zoneight234
    \\7pqrstsixteen
;

test "sample" {
    try std.testing.expectEqual(281, solve(SAMPLE));
}
