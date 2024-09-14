function U(e) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = e;
  return Object.keys(o).reduce((i, s) => {
    const r = s.match(/bind_(.+)_event/);
    if (r) {
      const l = r[1], c = l.split("_"), a = (...m) => {
        const d = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(l.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: d,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...n.props[c[f]] || {}
          };
          m[c[f]] = h, m = h;
        }
        const d = c[c.length - 1];
        return m[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = a, i;
      }
      const _ = c[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function I() {
}
function X(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Y(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return I;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function p(e) {
  let t;
  return Y(e, (o) => t = o)(), t;
}
const g = [];
function b(e, t = I) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(l) {
    if (X(e, l) && (e = l, o)) {
      const c = !g.length;
      for (const a of n)
        a[1](), g.push(a, e);
      if (c) {
        for (let a = 0; a < g.length; a += 2)
          g[a][0](g[a + 1]);
        g.length = 0;
      }
    }
  }
  function s(l) {
    i(l(e));
  }
  function r(l, c = I) {
    const a = [l, c];
    return n.add(a), n.size === 1 && (o = t(i, s) || I), l(e), () => {
      n.delete(a), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: r
  };
}
const {
  getContext: A,
  setContext: j
} = window.__gradio__svelte__internal, D = "$$ms-gr-antd-slots-key";
function L() {
  const e = b({});
  return j(D, e);
}
const Z = "$$ms-gr-antd-context-key";
function B(e) {
  var l;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = M(), o = J({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    o.slotKey.set(c);
  }), G();
  const n = A(Z), i = ((l = p(n)) == null ? void 0 : l.as_item) || e.as_item, s = n ? i ? p(n)[i] : p(n) : {}, r = b({
    ...e,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: a
    } = p(r);
    a && (c = c[a]), r.update((_) => ({
      ..._,
      ...c
    }));
  }), [r, (c) => {
    const a = c.as_item ? p(n)[c.as_item] : p(n);
    return r.set({
      ...c,
      ...a
    });
  }]) : [r, (c) => {
    r.set(c);
  }];
}
const F = "$$ms-gr-antd-slot-key";
function G() {
  j(F, b(void 0));
}
function M() {
  return A(F);
}
const H = "$$ms-gr-antd-component-slot-context-key";
function J({
  slot: e,
  index: t,
  subIndex: o
}) {
  return j(H, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(o)
  });
}
function Q(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var s = "", r = 0; r < arguments.length; r++) {
        var l = arguments[r];
        l && (s = i(s, n(l)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return o.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var r = "";
      for (var l in s)
        t.call(s, l) && s[l] && (r = i(r, l));
      return r;
    }
    function i(s, r) {
      return r ? s ? s + " " + r : s + r : s;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(V);
var T = V.exports;
const W = /* @__PURE__ */ Q(T), {
  getContext: $,
  setContext: tt
} = window.__gradio__svelte__internal;
function et(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(i = ["default"]) {
    const s = i.reduce((r, l) => (r[l] = b([]), r), {});
    return tt(t, {
      itemsMap: s,
      allowedSlots: i
    }), s;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: s
    } = $(t);
    return function(r, l, c) {
      i && (r ? i[r].update((a) => {
        const _ = [...a];
        return s.includes(r) ? _[l] = c : _[l] = void 0, _;
      }) : s.includes("default") && i.default.update((a) => {
        const _ = [...a];
        return _[l] = c, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: nt,
  getSetItemFn: st
} = et("anchor"), {
  SvelteComponent: it,
  check_outros: ot,
  component_subscribe: x,
  create_slot: rt,
  detach: lt,
  empty: ct,
  flush: y,
  get_all_dirty_from_scope: ut,
  get_slot_changes: ft,
  group_outros: at,
  init: _t,
  insert: mt,
  safe_not_equal: dt,
  transition_in: v,
  transition_out: k,
  update_slot_base: yt
} = window.__gradio__svelte__internal;
function q(e) {
  let t;
  const o = (
    /*#slots*/
    e[19].default
  ), n = rt(
    o,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), t = !0;
    },
    p(i, s) {
      n && n.p && (!t || s & /*$$scope*/
      262144) && yt(
        n,
        o,
        i,
        /*$$scope*/
        i[18],
        t ? ft(
          o,
          /*$$scope*/
          i[18],
          s,
          null
        ) : ut(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      t || (v(n, i), t = !0);
    },
    o(i) {
      k(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function bt(e) {
  let t, o, n = (
    /*$mergedProps*/
    e[0].visible && q(e)
  );
  return {
    c() {
      n && n.c(), t = ct();
    },
    m(i, s) {
      n && n.m(i, s), mt(i, t, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && v(n, 1)) : (n = q(i), n.c(), v(n, 1), n.m(t.parentNode, t)) : n && (at(), k(n, 1, 1, () => {
        n = null;
      }), ot());
    },
    i(i) {
      o || (v(n), o = !0);
    },
    o(i) {
      k(n), o = !1;
    },
    d(i) {
      i && lt(t), n && n.d(i);
    }
  };
}
function ht(e, t, o) {
  let n, i, s, r, l, {
    $$slots: c = {},
    $$scope: a
  } = t, {
    gradio: _
  } = t, {
    props: m = {}
  } = t;
  const d = b(m);
  x(e, d, (u) => o(17, l = u));
  let {
    _internal: f = {}
  } = t, {
    as_item: h
  } = t, {
    visible: C = !0
  } = t, {
    elem_id: K = ""
  } = t, {
    elem_classes: S = []
  } = t, {
    elem_style: w = {}
  } = t;
  const P = M();
  x(e, P, (u) => o(16, r = u));
  const [E, z] = B({
    gradio: _,
    props: l,
    _internal: f,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: w,
    as_item: h
  });
  x(e, E, (u) => o(0, s = u));
  const N = L();
  x(e, N, (u) => o(15, i = u));
  const R = st(), {
    default: O
  } = nt();
  return x(e, O, (u) => o(14, n = u)), e.$$set = (u) => {
    "gradio" in u && o(6, _ = u.gradio), "props" in u && o(7, m = u.props), "_internal" in u && o(8, f = u._internal), "as_item" in u && o(9, h = u.as_item), "visible" in u && o(10, C = u.visible), "elem_id" in u && o(11, K = u.elem_id), "elem_classes" in u && o(12, S = u.elem_classes), "elem_style" in u && o(13, w = u.elem_style), "$$scope" in u && o(18, a = u.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && d.update((u) => ({
      ...u,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    147264 && z({
      gradio: _,
      props: l,
      _internal: f,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: w,
      as_item: h
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $items*/
    114689 && R(r, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: W(s.elem_classes, "ms-gr-antd-anchor-item"),
        id: s.elem_id,
        ...s.props,
        ...U(s)
      },
      slots: i,
      children: n.length > 0 ? n : void 0
    });
  }, [s, d, P, E, N, O, _, m, f, h, C, K, S, w, n, i, r, l, a, c];
}
class pt extends it {
  constructor(t) {
    super(), _t(this, t, ht, bt, dt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  pt as default
};
