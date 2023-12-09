use gcd::Gcd;
use std::ops::BitAnd;

/// `UPS` represents an ultimately periodic set of natural numbers.
///
/// A `S` of natural numbers is _ultimately periodic_ if there are natural
/// numbers `n ≥ 0` and `p ≥ 1` such for all natural numbers `k ≥ n`, `k ∈ S`
/// if and only if `k + p ∈ S`. Every finite set `S` is ultimately periodic, as
/// can be seen by taking `n = 1 + max(S)` (or `n = 0` if `S` is empty) and
/// `p = 1`.
#[derive(Debug)]
pub struct UPS {
    // The number `n` from the definition.
    stem_len: u64,
    // The elemens of `S ∩ [0, n)` in increasing order.
    stem_elems: Vec<u64>,
    // The number p from the definition.
    loop_len: u64,
    // The elements of `S ∩ [n, n+p)` increasing order.
    loop_elems: Vec<u64>,
}

pub enum Iter<'a> {
    Stem {
        ups: &'a UPS,
        stem_index: usize,
    },
    Loop {
        ups: &'a UPS,
        loop_index: usize,
        offset: u64,
    },
}

impl UPS {
    /// `finite` constructs a finite `UPS` from a vector listing `S` in
    /// increasing order.
    pub fn finite(elems: Vec<u64>) -> Self {
        let stem_len = if let Some(last) = elems.last() {
            last + 1
        } else {
            0
        };
        Self {
            stem_len,
            stem_elems: elems,
            loop_len: 1,
            loop_elems: Vec::new(),
        }
    }

    /// `everything` returns the set of all natural numbers.
    pub fn everything() -> Self {
        Self {
            stem_len: 0,
            stem_elems: Vec::new(),
            loop_len: 1,
            loop_elems: vec![0],
        }
    }

    /// `from_prefix` constructs a `UPS` from `n`, `p` and a vector listing
    /// `S ∩ [0, n+p)` in increasing order.
    /// If `p == 0`, the function panics.
    /// If `prefix` is not in increasing order or contains elements greater
    /// than `n + p`, the function will succeed but the resulting `UPS` will
    /// not behave well.
    pub fn from_prefix(mut prefix: Vec<u64>, n: u64, p: u64) -> Self {
        if p == 0 {
            panic!("UPS::from_prefix: p most not be zero");
        }
        let i = prefix.binary_search(&n).unwrap_or_else(|i| i);
        let loop_elems = prefix.split_off(i);
        let stem_elems = prefix;
        Self {
            stem_len: n,
            stem_elems,
            loop_len: p,
            loop_elems,
        }
    }

    // Returns an iterator over the elements of `S` in increasing order.
    pub fn iter(&self) -> Iter {
        Iter::new(self)
    }

    fn combine<'a>(
        &'a self,
        other: &'a Self,
    ) -> (
        impl Iterator<Item = iter_set::Inclusion<u64>> + 'a,
        u64,
        u64,
    ) {
        let n = self.stem_len.max(other.stem_len);
        let d = self.loop_len.gcd(other.loop_len);
        let p = (self.loop_len / d)
            .checked_mul(other.loop_len)
            .expect("u64 overflow in UPS::combine");
        let n_p = n.checked_add(p).expect("u64 overflow in UPS::combine");
        let prefix =
            iter_set::classify(self.iter(), other.iter()).take_while(move |i| i.union() < n_p);
        (prefix, n, p)
    }
}

impl BitAnd for &UPS {
    type Output = UPS;

    fn bitand(self, other: Self) -> Self::Output {
        let (prefix, n, p) = self.combine(other);
        let prefix: Vec<_> = prefix.filter_map(|i| i.intersection()).collect();
        UPS::from_prefix(prefix, n, p)
    }
}

impl<'a> IntoIterator for &'a UPS {
    type Item = u64;
    type IntoIter = Iter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        Iter::new(self)
    }
}

impl<'a> Iter<'a> {
    fn new(ups: &'a UPS) -> Self {
        Iter::Stem { ups, stem_index: 0 }
    }
}

impl<'a> Iterator for Iter<'a> {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        match self {
            Iter::Stem { ups, stem_index } => {
                if let Some(k) = ups.stem_elems.get(*stem_index) {
                    *stem_index += 1;
                    Some(*k)
                } else {
                    if ups.loop_elems.is_empty() {
                        None
                    } else {
                        *self = Iter::Loop {
                            ups,
                            loop_index: 0,
                            offset: 0,
                        };
                        self.next()
                    }
                }
            }
            Iter::Loop {
                ups,
                loop_index,
                offset,
            } => {
                if let Some(k) = ups.loop_elems.get(*loop_index) {
                    *loop_index += 1;
                    k.checked_add(*offset)
                } else {
                    *offset = offset.checked_add(ups.loop_len)?;
                    *loop_index = 0;
                    self.next()
                }
            }
        }
    }
}

#[cfg(test)]
impl UPS {
    /// `identical` determines if two `UPS` have the internal representation.
    fn identical(&self, other: &Self) -> bool {
        self.stem_len == other.stem_len
            && self.stem_elems == other.stem_elems
            && self.loop_len == other.loop_len
            && self.loop_elems == other.loop_elems
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_iter() {
        let ups = UPS::from_prefix(vec![0, 2, 4, 6], 4, 3);
        let expected = UPS {
            stem_len: 4,
            stem_elems: vec![0, 2],
            loop_len: 3,
            loop_elems: vec![4, 6],
        };
        assert!(ups.identical(&expected));
    }

    #[test]
    fn test_iter() {
        let ups = UPS::from_prefix(vec![0, 2, 4, 6], 4, 3);
        let sample: Vec<_> = ups.iter().take(8).collect();
        assert_eq!(sample, vec![0, 2, 4, 6, 7, 9, 10, 12]);
    }

    #[test]
    fn test_intersection() {
        let ups1 = UPS::from_prefix(vec![0, 2, 4, 6], 4, 3);
        let ups2 = UPS::from_prefix(vec![2, 5, 7, 8, 10, 11, 13], 9, 6);
        let ups = &ups1 & &ups2;
        let expected = UPS {
            stem_len: 9,
            stem_elems: vec![2, 7],
            loop_len: 6,
            loop_elems: vec![10, 13],
        };
        assert!(ups.identical(&expected))
    }
}
